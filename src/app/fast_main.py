from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from fastapi.templating import Jinja2Templates
from pathlib import Path

from models import mongodb
from models.book import BookModel
from src.app.book_scraper import NaverBookScraper

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    # book = BookModel(keyword="파이썬", publisher="BJPublic", price=12000, image='test.png')
    # await mongodb.engine.save(book)
    return templates.TemplateResponse("index.html", {"request": request, "title": "책 수집기"})


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    # ?q=123
    # 1. 쿼리에서 검색어 추출
    keyword = q
    # 예외처리
    # - 검색어가 없다면 사용자에게 검색을 요구 return
    if not keyword:
        context = {"request": request, "title": "검색어가 없음"}
        return templates.TemplateResponse("index.html", context)
    # - 해당 검색어에 대해 수집된 데이터가 이미 DB 에 존재하면 DB 에서 꺼내와서 보여주고 Return
    if await mongodb.engine.find_one(BookModel, BookModel.keyword == keyword):
        books = await mongodb.engine.find(BookModel, BookModel.keyword == keyword)
        return templates.TemplateResponse("index.html", {"request": request, "title": "책을 찾아와줌", "books": books})

    naver_book_scraper = NaverBookScraper()
    books = await naver_book_scraper.search(keyword=keyword, total_page=10)
    book_models = []
    for book in books:
        print(book)
        book_models.append(BookModel(keyword=book["title"], publisher=book["publisher"], price=book["discount"], image=book["image"]))
    await mongodb.engine.save_all(book_models)
    return templates.TemplateResponse("index.html", {"request": request, "title": "책을 수집해줌", "books": book_models})


@app.on_event("startup")
def on_app_start():
    print("on_start_up_server")
    mongodb.connect()


@app.on_event("shutdown")
async def on_app_shutdown():
    mongodb.close()
    print("on_shutdown_server")
