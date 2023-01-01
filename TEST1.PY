import asyncio
from asyncio import Event, AbstractEventLoop
from datetime import datetime
import signal
from typing import Optional
from time import sleep
from concurrent.futures import FIRST_COMPLETED

async def s():
    while True:
           print("1")
           break
    return True


async def s2():
    while True:
           print("2")
    return

async def main_async():
    await asyncio.wait([s(), s2()], return_when=FIRST_COMPLETED)
    print("ok")
    return


asyncio.run(main_async())