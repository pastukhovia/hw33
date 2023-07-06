import string
import random
import time

from goals.models import Status, Goal, GoalCategory
from bot.models import TgUser

from ...tg.client import TgClient
import os


def generate_code(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choices(letters, k=length))


def commands(x, user, chat_id):
    match x:
        case '/goals':
            goals = Goal.objects.filter(
                category__board__participants__user=user.user
            ).exclude(status=Status.archived).select_related('user')
            tg_client.send_message(
                chat_id=chat_id,
                text="\n".join([goal.title for goal in goals])
            )
        case '/create':
            tg_client.send_message(
                chat_id=chat_id,
                text='Введите категорию из списка'
            )

            goal_categories = GoalCategory.objects.filter(
                board__participants__user=user.user,
                is_deleted=False
            ).select_related('user')

            category_names = [category.title for category in goal_categories]

            tg_client.send_message(
                chat_id=chat_id,
                text='\n'.join(category_names)
            )

            user_input = ''
            while user_input not in category_names:
                time.sleep(1)
                try:
                    user_input = tg_client.get_updates().result[-1]['message']['text']
                except:
                    tg_client.send_message(
                        chat_id=chat_id,
                        text='Неизвестная категория'
                    )
        case _:
            pass


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
            tg_client.send_message(chat_id=chat_id, text='Команда не найдена')

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
            try:
                commands(user_input, cur_user, chat_id)
            except Exception as e:
                tg_client.send_message(
                    chat_id=chat_id,
                    text=f'{e}'
                )
