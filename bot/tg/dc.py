from dataclasses import dataclass, field
from typing import List


@dataclass
class MessageFrom:
    id: int
    is_bot: bool
    first_name: str
    username: str
    language_code: str = ''


@dataclass
class Chat:
    id: int
    first_name: str
    username: str
    type: str


@dataclass
class Message:
    message_id: int
    date: int
    text: str
    message_from: MessageFrom
    chat: Chat


@dataclass
class UpdateObj:
    update_id: int
    message: Message
    chat: Chat
    date: int
    text: str


@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj] = field(default_factory=list)


@dataclass
class SendMessageResponse:
    ok: bool
    result: Message
