import time

from bs4 import BeautifulSoup
import aiohttp
import asyncio


async def fetch(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as response:
        body_html = await response.text()
        soup = BeautifulSoup(body_html, 'html.parser')
        cont_thumb = soup.find_all("div", 'cont_thumb')
        for div in cont_thumb:
            title = div.find("p", "txt_thumb")
            if title is not None:
                print(title.text)


async def main():
    BASE_URL = "https://bjpublic.tistory.com/category/%EC%A0%84%EC%B2%B4%20%EC%B6%9C%EA%B0%84%20%EB%8F%84%EC%84%9C?"
    urls = [f"{BASE_URL}page={i}" for i in range(1, 10)]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, url) for url in urls])


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time() - start_time
    print(end_time)
