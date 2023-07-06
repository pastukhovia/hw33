import os

from bot.models import TgUser

from .utils import commands, generate_code
from ...tg.client import TgClient

offset = 0
tg_client = TgClient(os.getenv('TG_BOT_KEY'))
while True:
    res = tg_client.get_updates(offset=offset)
    for item in res.result:
        offset = item['update_id'] + 1
        chat_id = item['message']['chat']['id']
        tg_user = item['message']['from']['username']
        try:
            user_input = item['message']['text']
        except:
            item['message']['text'] = ''

        cur_user, created = TgUser.objects.get_or_create(
            tg_user=tg_user,
            tg_chat=chat_id
        )

        if created:
            tg_client.send_message(chat_id=chat_id, text='Добро пожаловать!')
            verification_code = generate_code(15)
            while TgUser.objects.filter(verification_code=verification_code).exists():
                verification_code = generate_code(15)
            cur_user.verification_code = verification_code
            cur_user.save()

        if cur_user.user_id is None:
            tg_client.send_message(
                chat_id=chat_id,
                text=f'Подтвердите, пожалуйста, свой аккаунт. '
                     f'Для подтверждения необходимо ввести код: {cur_user.verification_code} на сайте'
            )
        else:
            commands(user_input, cur_user, chat_id)
