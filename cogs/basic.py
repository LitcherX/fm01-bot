from time import perf_counter

from discord.ext import commands

from core import Context, Bot


class Basic(commands.Cog, name="Basic"):
	def __init__(self, client: Bot):
		self.client = client

	@commands.hybrid_command(name="ping", description="ping_specs-description")
	async def ping(self, ctx: Context):
		# Database ping calculation
		database_start = perf_counter()
		await self.client.db.execute("SELECT 1")
		database = perf_counter() - database_start

		await ctx.send("ping", latency=float(self.client.latency), db=float(database))

	@commands.command()
	async def raiseerror(self, ctx: Context):
		raise Exception("This is a test exception for error handling.")


async def setup(client: Bot):
	await client.add_cog(Basic(client))
