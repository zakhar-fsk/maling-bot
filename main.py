from fastapi import FastAPI
from config import settings
from services.userbot import UserBot

app = FastAPI()


@app.get("/")
async def root():
    bot = UserBot(settings.APP_ID, settings.APP_HASH)
    return {"bot_object": bot}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
