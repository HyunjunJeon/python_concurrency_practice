import time
import os

import aiohttp
import asyncio
import aiofiles

from config import get_secret


async def image_downloader(session: aiohttp.ClientSession, img: str) -> None:
    img_name = img.split("/")[-1]
    if not img_name.endswith("jpg"):
        return

    try:
        os.mkdir("./images")
    except FileExistsError:
        pass

    async with session.get(img) as response:
        if response.status == 200:
            async with aiofiles.open(f"./images/{img_name}", mode='wb') as f:
                img_data = await response.read()
                await f.write(img_data)


async def fetch(session: aiohttp.ClientSession, url: str, i: int) -> None:
    naver_api_headers = {
        "X-Naver-Client-Id": get_secret("NAVER_API_ID"),
        "X-Naver-Client-Secret": get_secret("NAVER_API_SECRET")
    }
    async with session.get(url, headers=naver_api_headers) as response:
        json_data = await response.json()
        _items = json_data["items"]
        _images = [item["link"] for item in _items]
        await asyncio.gather(*[image_downloader(session, img_src) for img_src in _images])


async def main() -> None:
    NAVER_IMAGE_BASE_URL = "https://openapi.naver.com/v1/search/image"
    keyword = "dog"
    display = 20
    urls = [f"{NAVER_IMAGE_BASE_URL}?query={keyword}&display={display}&start={1 + i * display}" for i in range(10)]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, url, i) for i, url in enumerate(urls)])


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time() - start_time
    print(end_time)
