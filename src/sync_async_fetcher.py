import asyncio
import time

import aiohttp
import requests

urls = ["https://naver.com", "https://google.com", "https://instagram.com"] * 10


def fetcher_sync(session, url):
    with session.get(url) as response:
        return response.text


def main_sync():
    with requests.Session() as session:
        result = [fetcher_sync(session, url) for url in urls]
        print(result)


async def fetcher_async(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main_async():
    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(*[fetcher_async(session, url) for url in urls])  # unpacking 해서 넘겨줌
        print(result)


if __name__ == "__main__":
    start_time = time.time()
    # main_sync()  # 11.99048900604248
    asyncio.run(main_async())  # 1.165215015411377
    end_time = time.time() - start_time
    print(end_time)  # 11.99048900604248
