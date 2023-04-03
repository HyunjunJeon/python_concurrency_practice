from src.app.project_config import NAVER_API_ID, NAVER_API_SECRET
import aiohttp
import asyncio


class NaverBookScraper:
    NAVER_API_BOOK = "https://openapi.naver.com/v1/search/book.json"

    @staticmethod
    async def fetch(session, url, headers):
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                return result["items"]

    def unit_url(self, keyword: str, start: int):
        return {
            "url": f"{self.NAVER_API_BOOK}?query={keyword}&display=10&start={start}",
            "headers": {
                "X-Naver-Client-Id": NAVER_API_ID,
                "X-Naver-Client-Secret": NAVER_API_SECRET
            },
        }

    async def search(self, keyword: str, total_page: int):
        apis = [self.unit_url(keyword=keyword, start=(1 + i * 10)) for i in range(total_page)]
        async with aiohttp.ClientSession() as session:
            all_data = await asyncio.gather(
                *[NaverBookScraper.fetch(session, api["url"], api["headers"]) for api in apis]
            )
            result = []
            for data in all_data:
                if data is not None:
                    for book in data:
                        result.append(book)
            return result

    def run(self, keyword: str, total_page: int):
        return asyncio.run(self.search(keyword, total_page))


# if __name__ == '__main__':
#     scraper = NaverBookScraper()
#     data = scraper.run("파이썬", 2)
#     print(data)
#     print(len(data))