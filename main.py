import argparse
import asyncio
import os

from core.bot import Bot
from core.logger import logger
from dotenv import load_dotenv

try:
	import uvloop  # type: ignore

	asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
	if os.name == "nt":
		asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
	else:
		asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

parser = argparse.ArgumentParser(prog="fm01")
parser.add_argument("--debug", action="store_true")


async def main(debug=False) -> None:
	logger.info("Starting the bot...")
	load_dotenv()

	client = Bot()
	client.debug = debug

	if client.debug:
		token = os.getenv("DEBUG_TOKEN")
		logger.info("Running in debug mode")
	else:
		token = os.getenv("TOKEN")
		logger.info("Running in production mode")

	if token:
		await client.start(token)
	else:
		logger.error("Token not found")


if __name__ == "__main__":
	args = parser.parse_args()
	asyncio.run(main(args.debug))
