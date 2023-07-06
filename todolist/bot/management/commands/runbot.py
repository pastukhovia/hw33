import string
import random

from ...models import TgUser
from ...tg.client import TgClient


def generate_code(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choices(letters, k=length))


offset = 0
tg_client = TgClient("6377852173:AAFnrvVc02xpxDg09tgG2KjrbniRPik_VyU")
while True:
    res = tg_client.get_updates(offset=offset)
    for item in res.result:
        offset = item['update_id'] + 1
        cur_user, created = TgUser.objects.get_or_create(
            tg_user=item['message']['from']['username'],
            tg_chat=item['message']['chat']['id']
        )

        if created:
            tg_client.send_message(chat_id=item['message']['chat']['id'], text='Добро пожаловать!')
            verification_code = generate_code(15)
            while TgUser.objects.filter(verification_code=verification_code).exists():
                verification_code = generate_code(15)
            cur_user.verification_code = verification_code
            cur_user.save()

        if cur_user.user_id is None:
            tg_client.send_message(
                chat_id=item['message']['chat']['id'],
                text=f'Подтвердите, пожалуйста, свой аккаунт. '
                     f'Для подтверждения необходимо ввести код: {cur_user.verification_code} на сайте'
            )
