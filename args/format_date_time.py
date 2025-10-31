import datetime

import discord
from args.formattable import Formattable


class FormatDateTime:
	"""Formats a datetime object into a dynamic Discord timestamp.

	You have to specify a default style, which will be used if no style is provided by the end user.
	This is needed because by passing this class as a value for a property, users can call it with or without brackets.
	So for example, ``created_at``, ``created_at()`` and ``created_at("long")`` will all work. The one without the
	brackets will always use the default style.
	"""

	def __init__(self, data: datetime.datetime, default_style: discord.utils.TimestampStyle):
		self.data = data
		self.default_style = default_style

	@property
	def timestamp(self) -> str:
		return self.data.astimezone(datetime.timezone.utc).replace(tzinfo=None).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

	@property
	def time(self) -> Formattable:
		"""Returns the hours and minutes of the timestamp.

		Examples
		--------
		>>> FormatDateTime(datetime.datetime.now(), "F").time
		22:57
		"""
		return Formattable(self, style="f")

	@property
	def seconds(self) -> Formattable:
		"""Returns the seconds of the timestamp.

		Examples
		--------
		>>> FormatDateTime(datetime.datetime.now(), "F").seconds
		22:57:43
		"""
		return Formattable(self, style="f")

	@property
	def date(self) -> Formattable:
		"""Returns the date of the timestamp.

		Examples
		--------
		>>> FormatDateTime(datetime.datetime.now(), "F").date
		2022-02-17
		"""
		return Formattable(self, style="D")

	@property
	def short(self) -> Formattable:
		"""Returns the short version of the timestamp.

		Examples
		--------
		>>> FormatDateTime(datetime.datetime.now(), "F").short
		17 Feb 2022
		"""
		return Formattable(self, style="f")

	@property
	def long(self) -> Formattable:
		"""Returns the long version of the timestamp.

		Examples
		--------
		>>> FormatDateTime(datetime.datetime.now(), "F").long
		Thursday, 17 February 2022
		"""
		return Formattable(self, style="F")

	@property
	def relative(self) -> Formattable:
		"""Returns the relative version of the timestamp.

		Examples
		--------
		>>> FormatDateTime(datetime.datetime.now(), "F").relative
		1 minute ago
		"""
		return Formattable(self, style="R")

	def __repr__(self) -> str:
		return Formattable(self, style=self.default_style).value
