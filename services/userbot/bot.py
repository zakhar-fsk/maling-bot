from loguru import logger
from telethon import functions, TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.sessions import StringSession


class UserBotSettings:
    @logger.catch
    def __init__(self):
        self.user_client: TelegramClient | None = None
        self._app_id: int | None = None
        self._app_hash: str | None = None
        self._phone_number: str | None = None
        self._need_password: bool = False

    @property
    def app_id(self):
        return self._app_id

    @app_id.setter
    def app_id(self, value: int):
        self._app_id = value

    @property
    def app_hash(self):
        return self._app_hash

    @app_hash.setter
    def app_hash(self, value):
        self._app_hash = value

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value):
        self._phone_number = value

    @property
    def need_password(self):
        return self._need_password

    @need_password.setter
    def need_password(self, value):
        self._need_password = value


class UserBot(UserBotSettings):
    @logger.catch
    def __init__(self):
        super().__init__()

    @logger.catch
    async def init_client(self):
        self.user_client = TelegramClient(StringSession("session"), self._app_id, self._app_hash)

    @classmethod
    async def create(cls, api_id: str, api_hash: str) -> 'UserBot':
        self = cls(api_id, api_hash)
        await self.user_client.connect()
        return self

    @logger.catch
    async def authorize(self):
        await self.init_client()
        await self.user_client.connect()

        if not await self.user_client.is_user_authorized():
            await self.user_client.send_code_request(self._phone_number)

    @logger.catch
    async def sign_in(self, code: str):
        try:
            await self.user_client.sign_in(self._phone_number, code)
            logger.info("Sign in success")
            return {"status": "success", "password_needed": False}
        except SessionPasswordNeededError:
            logger.info("Password is needed")
            self._need_password = True
            return {"status": "success", "password_needed": True}

    @logger.catch
    async def sign_in_password(self, password: str):
        try:
            await self.user_client.sign_in(password=password)
        except Exception as e:
            logger.exception(e)

    @logger.catch
    async def send_message(self, chat_id, message):
        await self.user_client.send_message(chat_id, message)

    @logger.catch
    async def get_list_groups(self):
        return [dialog for dialog in await self.user_client.get_dialogs() if dialog.is_group]

    @logger.catch
    async def get_group_by_name(self, name):
        result = await self.user_client(functions.contacts.SearchRequest(q=name, limit=1))
        logger.info(result)
