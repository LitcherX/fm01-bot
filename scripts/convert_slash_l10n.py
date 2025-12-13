#!/usr/bin/env python3
"""
Convert old slash localization structure (separate `<base>` and `<base>_specs`) into single-object style used by the project.

Old:
  "afk": "afk",
  "afk_specs": {"description":..., "args": {...}}

New:
  "afk": {"name": "afk", "desc": ..., "args": {...}}

Usage:
  python scripts/convert_slash_l10n.py path/to/file.json --inplace
  python scripts/convert_slash_l10n.py dir/ --recursive --inplace

The script will create a backup file with suffix `.bak` when using `--inplace`.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any, Dict, Optional


def transform_one(obj: Dict[str, Any]) -> Dict[str, Any]:
	out = dict(obj)  # shallow copy
	keys = list(obj.keys())

	for k in keys:
		# detect specs keys like "foo_specs" or "foo-specs"
		if k.endswith("_specs") or k.endswith("-specs") or k.endswith("_spec") or k.endswith("-spec"):
			base = (
				k.rsplit("_specs", 1)[0]
				if "_specs" in k
				else (
					k.rsplit("-specs", 1)[0]
					if "-specs" in k
					else (k.rsplit("_spec", 1)[0] if "_spec" in k else k.rsplit("-spec", 1)[0])
				)
			)
			specs = obj.get(k)
			if not isinstance(specs, dict):
				continue

			# If base already is an object (new format), skip
			existing = obj.get(base)
			if isinstance(existing, dict):
				# optionally merge missing fields from specs
				continue

			name_value = None
			if isinstance(existing, str):
				name_value = existing
			name_value = specs.get("name") or name_value or base

			desc_value = specs.get("description") or specs.get("desc")
			usage_value = specs.get("usage")

			args_src = specs.get("args") or specs.get("arguments") or {}
			args_out: Dict[str, Dict[str, Any]] = {}
			if isinstance(args_src, dict):
				for an, av in args_src.items():
					if isinstance(av, dict):
						arg_name = av.get("name", an)
						arg_desc = av.get("description") or av.get("desc")
						new_av: Dict[str, Any] = {"name": arg_name}
						if arg_desc is not None:
							new_av["desc"] = arg_desc
						# Preserve other keys from original arg (except description/name)
						for fk, fv in av.items():
							if fk in ("name", "description", "desc"):
								continue
							new_av[fk] = fv
						args_out[an] = new_av
					else:
						args_out[an] = {"name": an}

			# Build new command object
			new_obj: Dict[str, Any] = {}
			new_obj["name"] = name_value
			if desc_value is not None:
				new_obj["desc"] = desc_value
			if usage_value is not None:
				new_obj["usage"] = usage_value

			# Copy remaining fields from specs (excluding handled ones)
			for fk, fv in specs.items():
				if fk in ("name", "description", "desc", "usage", "args", "arguments"):
					continue
				new_obj[fk] = fv

			if args_out:
				new_obj["args"] = args_out

			out[base] = new_obj

			# remove old specs key and old top-level string if present
			if k in out:
				del out[k]
			if isinstance(existing, str) and base in out and out[base].get("name") == existing:
				# we already kept name in the new obj; nothing else to remove
				pass

	return out


def process_file(path: Path, inplace: bool = False, backup: bool = True) -> Path:
	data = json.loads(path.read_text(encoding="utf-8"))
	if not isinstance(data, dict):
		raise ValueError(f"Expected top-level object in {path}")

	new_data = transform_one(data)

	if inplace:
		if backup:
			bak = path.with_suffix(path.suffix + ".bak")
			shutil.copy2(path, bak)
		path.write_text(json.dumps(new_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
		return path
	else:
		out = path.with_name(path.stem + ".converted" + path.suffix)
		out.write_text(json.dumps(new_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
		return out


def main() -> None:
	parser = argparse.ArgumentParser(description="Convert slash localization JSON files to single-object style.")
	parser.add_argument("paths", nargs="+", help="Files or directories to process")
	parser.add_argument("--recursive", "-r", action="store_true", help="Recurse into directories")
	parser.add_argument("--inplace", "-i", action="store_true", help="Overwrite original files (creates .bak) ")
	parser.add_argument("--ext", default=".json", help="File extension to match when processing directories")
	args = parser.parse_args()

	files = []
	for p in args.paths:
		p = Path(p)
		if p.is_dir():
			if args.recursive:
				files.extend([f for f in p.rglob(f"*{args.ext}") if f.is_file()])
			else:
				files.extend([f for f in p.glob(f"*{args.ext}") if f.is_file()])
		elif p.is_file():
			files.append(p)
		else:
			print(f"Path not found: {p}")

	if not files:
		print("No files found")
		return

	for f in files:
		try:
			out = process_file(f, inplace=args.inplace)
			print(f"Converted: {f} -> {out}")
		except Exception as e:
			print(f"Failed: {f}: {e}")


if __name__ == "__main__":
	main()
