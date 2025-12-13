import random
from urllib.parse import quote_plus

import discord
from art import text2art
from core import Context, Bot
from discord import app_commands
from discord.ext import commands
from helpers import CustomResponse
from helpers.convert import text_to_emoji
from helpers.regex import DISCORD_MESSAGE_URL


class Say(commands.Cog, name="Says"):
	def __init__(self, client: Bot):
		self.client = client
		self.custom_response: CustomResponse = CustomResponse(client)

	@commands.hybrid_group(name="say", description="say-desc", fallback="say-fallback", usage="say-usage")
	@commands.has_permissions(manage_messages=True)
	@app_commands.rename(message="say-args-message-name")
	@app_commands.describe(message="say-args-message-desc")
	async def say(self, ctx: Context, *, message: commands.Range[str, 1, 2000]):
		await ctx.send("say.message", message=message)

	@say.command(name="channel", description="chsay-desc", usage="chsay-usage")
	@commands.has_permissions(manage_messages=True)
	@app_commands.rename(channel="chsay-args-channel-name", message="chsay-args-message-name")
	@app_commands.describe(channel="chsay-args-channel-desc", message="chsay-args-message-desc")
	async def channel_say(self, ctx: Context, channel: discord.TextChannel, *, message: commands.Range[str, 1, 2000]):
		await channel.send(message, allowed_mentions=discord.AllowedMentions.none())

	@say.command(name="edit", description="editmsg-desc", usage="editmsg-usage")
	@commands.has_permissions(manage_messages=True)
	@app_commands.rename(message_link="editmsg-args-link-name", content="editmsg-args-content-name")
	@app_commands.describe(message_link="editmsg-args-link-desc", content="editmsg-args-content-desc")
	async def edit_message(self, ctx: Context, message_link: str, *, content: commands.Range[str, 1, 2000]):
		match = DISCORD_MESSAGE_URL.search(message_link)
		try:
			if match:
				guild_id, channel_id, message_id = match.groups()
				message = await self.client.get_channel(int(channel_id)).fetch_message(int(message_id))
			else:
				message = await ctx.channel.fetch_message(int(message_link))
		except (discord.NotFound, discord.Forbidden):
			raise commands.BadArgument("message_link")
		try:
			await message.edit(content=content, allowed_mentions=discord.AllowedMentions.none())
		except discord.Forbidden:
			raise commands.MissingPermissions(["manage_messages"])
		except discord.NotFound:
			raise commands.BadArgument("message_link")
		await ctx.send("say.edit")

	@say.command(name="ascii", description="asciisay-desc", usage="asciisay-usage")
	@commands.has_permissions(manage_messages=True)
	@app_commands.rename(message="asciisay-args-message-name")
	@app_commands.describe(message="asciisay-args-message-desc")
	async def ascii_say(self, ctx: Context, *, message: commands.Range[str, 1, 20]):
		await ctx.send("say.ascii", ascii=text2art(message))

	@say.command(name="emoji", description="emojisay-desc", usage="emojisay-usage")
	@commands.has_permissions(manage_messages=True)
	@app_commands.rename(message="emojisay-args-message-name")
	@app_commands.describe(message="emojisay-args-message-desc")
	async def emoji_say(self, ctx: Context, *, message: commands.Range[str, 1, 20]):
		await ctx.send("say.emoji", emoji=" ".join(text_to_emoji(message)))

	@say.command(name="achievement", description="mcsay-desc", usage="mcsay-usage")
	@commands.has_permissions(manage_messages=True)
	@app_commands.rename(message="mcsay-args-message-name")
	@app_commands.describe(message="mcsay-args-message-desc")
	async def achievement_say(self, ctx: Context, *, message: commands.Range[str, 1, 50]):
		icon = random.randint(1, 29)
		localized_title = await self.custom_response("say.achievement.title", ctx)
		achievement_title = quote_plus(localized_title)
		achievement_text = quote_plus(message)
		url = f"https://skinmc.net/achievement/{icon}/{achievement_title}/{achievement_text}"
		await ctx.send("say.achievement.response", achievement=url)

	@say.command(name="qr", description="qr-desc", usage="qr-usage")
	@commands.has_permissions(manage_messages=True)
	@app_commands.rename(data="qr-args-data-name")
	@app_commands.describe(data="qr-args-data-desc")
	async def qr_code(self, ctx: Context, *, data: commands.Range[str, 1, 500]):
		data = quote_plus(data)
		qr = f"https://api.qrserver.com/v1/create-qr-code/?data={data}&size=1000x1000&qzone=2"
		await ctx.send("say.qr", qr=qr)

	@say.command(name="reverse", description="reversesay-desc", usage="reversesay-usage")
	@commands.has_permissions(manage_messages=True)
	@app_commands.rename(message="reversesay-args-msg-name")
	@app_commands.describe(message="reversesay-args-msg-desc")
	async def reverse_say(self, ctx: Context, *, message: commands.Range[str, 1, 2000]):
		await ctx.send("say.reverse", message=message[::-1])

	@say.command(name="clap", description="clapsay-desc", usage="clapsay-usage")
	@commands.has_permissions(manage_messages=True)
	@app_commands.rename(message="clapsay-args-message-name")
	@app_commands.describe(message="clapsay-args-message-desc")
	async def clap_say(self, ctx: Context, *, message: commands.Range[str, 1, 500]):
		await ctx.send("say.clap", message=message.replace(" ", "👏"))


async def setup(client: Bot):
	await client.add_cog(Say(client))
