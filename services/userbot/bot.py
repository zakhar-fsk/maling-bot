from telethon import TelegramClient


class UserBot:
    def __init__(self, api_id, api_hash):
        self.client = TelegramClient('session', api_id, api_hash)

    async def send_message(self, chat_id, message):
        await self.client.send_message(chat_id, message)
