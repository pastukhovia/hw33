import requests

from .dc import GetUpdatesResponse, SendMessageResponse


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        method = f'getUpdates?offset={offset}&timeout={timeout}'
        return GetUpdatesResponse(**requests.get(self.get_url(method)).json())

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        method = f'sendMessage?chat_id={chat_id}&text={text}'
        return SendMessageResponse(**requests.get(self.get_url(method)).json())
