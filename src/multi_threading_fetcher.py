import os
import threading
import time

import requests

from concurrent.futures.thread import ThreadPoolExecutor

urls = ["https://naver.com", "https://google.com", "https://instagram.com"] * 10


def fetcher_sync(param):
    session = param[0]
    url = param[1]
    print(f"{os.getpid()} process | {threading.get_ident()} url: {url}")
    with session.get(url) as response:
        return response.text


def multi_thread_main_sync():

    executor = ThreadPoolExecutor(max_workers=10)

    with requests.Session() as session:
        # result = [fetcher_sync(session, url) for url in urls]
        # print(result)
        params = [(session, url) for url in urls]  # session 과 url 을 가진 리스트로 새로 만들어서 넣어줌
        result = list(executor.map(fetcher_sync, params))
        print(result)


if __name__ == "__main__":
    start_time = time.time()
    multi_thread_main_sync()
    end_time = time.time() - start_time
    print(end_time)
