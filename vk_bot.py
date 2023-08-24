import logging
import random

from environs import Env
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow_api import get_dialogflow_answer
from log_handler import TelegramLogsHandler


logger = logging.getLogger(__name__)


def send_reply(event, bot, project_id):
    try:
        query_result = get_dialogflow_answer(
            event.user_id,
            event.text,
            project_id,
        )
        if not query_result.intent.is_fallback:
            bot.messages.send(
                user_id=event.user_id,
                message=query_result.fulfillment_text,
                random_id=random.randint(1,1000),
            )
    except Exception as e:
        logger.exception(e)


def main():
    env = Env()
    env.read_env()

    if env('TG_LOGBOT_TOKEN', None) and env('ADMIN_TG_CHAT_ID', None):
        handler = TelegramLogsHandler(env('TG_LOGBOT_TOKEN'), env('ADMIN_TG_CHAT_ID'))
    else:
        handler = logging.StreamHandler()

    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    vk_session = vk_api.VkApi(token=env('VK_TOKEN'))
    bot = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    logger.info('Bot vk_bot started')

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                send_reply(event, bot, env('GOOGLE_CLOUD_PROJECT'))
            except Exception as e:
                logger.exception(e)


if __name__ == "__main__":
    main()
