from fastapi import FastAPI
from loguru import logger
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from config import settings
from services.userbot import UserBot

logger.add(
    "logs/file_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {module}:{function}:{line} | {message}",
    level="DEBUG",
    enqueue=True,
    backtrace=True
)

app = FastAPI()
templates = Jinja2Templates(directory="./templates")
client = UserBot()

# TODO: Додати обробку помилок, коли треба ввести пароль коли ні
# TODO: При відприавці коду треба ше відправити номер телефону, можна додавати ці поля в клас UserBot


@app.get("/")
@logger.catch
async def root(request: Request):
    context = {
        "account_connected": client.user_client is not None and await client.user_client.is_user_authorized(),
        "need_password": client.need_password,
    }
    logger.info(client.user_client)

    if client.user_client is not None and await client.user_client.is_user_authorized():
        context["groups"] = await client.get_list_groups()

    return templates.TemplateResponse(
        request=request,
        name="form.html",
        context=context
    )


@app.post("/send_auth_code")
@logger.catch
async def send_auth_code(request: Request):
    logger.info(f'send_auth_code - {await request.form()}')
    form_data = await request.form()

    client.app_id = int(form_data.get("app_id"))
    client.app_hash = form_data.get("app_hash")
    client.phone_number = form_data.get("phone_number")

    await client.authorize()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/account_signin")
@logger.catch
async def account_signin(request: Request):
    logger.info(f'account_signin - {await request.form()}')
    form_data = await request.form()
    await client.sign_in(form_data.get("code"))
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/send_message")
@logger.catch
async def send_message(request: Request):
    logger.info(f'send_message - {await request.form()}')
    form_data = await request.form()
    await client.get_group_by_name(form_data.get("group_name"))
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/sign_out")
@logger.catch
async def sign_out():
    logger.info(
        f"sign_out - {client.user_client is not None and client.user_client.is_connected() and await client.user_client.is_user_authorized()}")
    if client.user_client is not None and client.user_client.is_connected() and await client.user_client.is_user_authorized():
        await client.user_client.disconnect()
    else:
        logger.info("Client is not connected")

    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
