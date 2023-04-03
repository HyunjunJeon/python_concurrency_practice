from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from src.app.project_config import MONGO_URL, MONGO_DB_NAME


class MongoDB:
    def __init__(self):
        self.__client = None
        self.__engine = None

    def connect(self):
        self.__client = AsyncIOMotorClient(MONGO_URL)
        self.__engine = AIOEngine(client=self.__client, database=MONGO_DB_NAME)
        print("connected to Mongo DB")

    @property
    def engine(self) -> AIOEngine:
        return self.__engine

    @property
    def client(self) -> AsyncIOMotorClient:
        return self.__client

    def close(self):
        self.client.close()


mongodb = MongoDB()
