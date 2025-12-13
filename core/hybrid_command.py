import inspect
from typing import TYPE_CHECKING, Any, Callable, Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from core.slash_localization import slash_command_localization

if TYPE_CHECKING:
	from discord.ext.commands.hybrid import CogT, CommandCallback, Context, P, T, Unpack, _HybridCommandKwargs


type Permission = Literal[
	"add_reactions",
	"administrator",
	"attach_files",
	"ban_members",
	"change_nickname",
	"connect",
	"create_events",
	"create_expressions",
	"create_instant_invite",
	"create_polls",
	"create_private_threads",
	"create_public_threads",
	"deafen_members",
	"embed_links",
	"external_emojis",
	"external_stickers",
	"kick_members",
]


class HybridCommand(commands.HybridCommand):
	def __init__(
		self,
		func: "CommandCallback[CogT, Context[Any], P, T]",
		/,
		name: Any,
		description: Any,
		permissions: list[Permission] = None,
		**kwargs: "Unpack[_HybridCommandKwargs]",
	):
		super().__init__(func, name=name, description=description, **kwargs)
		self.permissions = permissions

		if permissions:
			perms_dict = {perm: True for perm in permissions}
			self.checks.append(commands.has_permissions(**perms_dict).predicate)
			if self.app_command:
				self.app_command.checks.append(app_commands.checks.has_permissions(**perms_dict).predicate)


def command(
	name: str | None = None,
	*,
	description: str | None = None,
	with_app_command: bool = True,
	permissions: list[discord.Permissions] | None = None,
	nsfw: bool = False,
	guild_only: bool = False,
	hidden: bool = False,
	# Optional base key used for localization lookups. If not provided
	# we fall back to `name` or the function name.
	l10n_key: str | None = None,
) -> Callable[["CommandCallback[CogT, Context[Any], P, T]"], HybridCommand]:
	def decorator(func: "CommandCallback[CogT, Context[Any], P, T]") -> HybridCommand:
		if isinstance(func, commands.Command):
			raise TypeError("Callback is already a command")

		# Decide localization base key priority: explicit l10n_key > provided name > function name
		base = l10n_key or name or func.__name__

		# Use provided description or fallback to english description if available
		text_description = description or f"{base}-desc"

		usage = f"{base}-usage"

		cmd = HybridCommand(
			func,
			name=base,
			description=text_description,
			usage=usage,
			with_app_command=with_app_command,
			permissions=permissions or [],
			nsfw=nsfw,
			guild_only=guild_only,
			hidden=hidden,
		)

		# Attach localizations to the app command in JSON-serializable form
		if cmd.app_command:
			cmd.app_command.name = f"{base}-name"
			cmd.app_command.description = f"{base}-desc"

			for param in cmd.app_command._params.values():
				param_name = param.display_name
				param._rename = f"{base}-args-{param_name}-name"
				param.description = f"{base}-args-{param_name}-desc"

			cmd.app_command._convert_to_locale_strings()

		print(base)

		return cmd

	return decorator
