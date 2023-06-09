import os
import secrets
import string
import time

from goals.models import Status, Goal, GoalCategory
from ...tg.client import TgClient

tg_client = TgClient(os.getenv('TG_BOT_KEY'))


def generate_code(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))


def commands(x, user, chat_id):
    match x:
        case '/goals':
            try:
                goals = Goal.objects.filter(
                    category__board__participants__user=user.user
                ).exclude(status=Status.archived).select_related('user')

                tg_client.send_message(
                    chat_id=chat_id,
                    text="\n".join([goal.title for goal in goals])
                )
            except:
                tg_client.send_message(
                    chat_id=chat_id,
                    text='У вас нет созданных целей'
                )
                return 1
        case '/create':
            tg_client.send_message(
                chat_id=chat_id,
                text='Введите категорию из списка'
            )

            try:
                goal_categories = GoalCategory.objects.filter(
                    board__participants__user=user.user,
                    is_deleted=False
                ).select_related('user')

                category_names = [category.title for category in goal_categories]

                tg_client.send_message(
                    chat_id=chat_id,
                    text='\n'.join(category_names)
                )
            except:
                tg_client.send_message(
                    chat_id=chat_id,
                    text='У вас нет созданных категорий'
                )
                return 1

            category_input = ''
            while category_input not in category_names:
                time.sleep(0.5)
                try:
                    category_input = tg_client.get_updates().result[-1]['message']['text']
                except:
                    tg_client.get_updates().result[-1]['message']['text'] = ''
                if category_input == '/cancel':
                    tg_client.send_message(
                        chat_id=chat_id,
                        text='Операция отменена'
                    )
                    return 1

            goal_category = GoalCategory()
            for category in goal_categories:
                if category.title == category_input:
                    goal_category = category

            tg_client.send_message(
                chat_id=chat_id,
                text="Введите название цели"
            )

            goal_input = category_input
            while goal_input == category_input:
                time.sleep(0.5)
                try:
                    goal_input = tg_client.get_updates().result[-1]['message']['text']
                except:
                    tg_client.get_updates().result[-1]['message']['text'] = ''
                if goal_input == '/cancel':
                    tg_client.send_message(
                        chat_id=chat_id,
                        text='Операция отменена'
                    )
                    return 1

            Goal.objects.create(user=user.user, title=goal_input, category=goal_category)

            tg_client.send_message(
                chat_id=chat_id,
                text="Цель создана"
            )
        case _:
            pass
