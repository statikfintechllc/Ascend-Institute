# openhands_wrapper.py
import asyncio
from openhands.core.cli import main


def run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
