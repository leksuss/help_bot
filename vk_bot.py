import logging
import random

from environs import Env
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow_api import get_dialogflow_answer


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def send_reply(event, bot, project_id):
    reply = get_dialogflow_answer(
        event.user_id,
        event.text,
        project_id,
        is_fallback=True
    )
    bot.messages.send(
        user_id=event.user_id,
        message=reply,
        random_id=random.randint(1,1000),
    )


def main():
    env = Env()
    env.read_env()

    vk_session = vk_api.VkApi(token=env('VK_TOKEN'))
    bot = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_reply(event, bot, env('GOOGLE_CLOUD_PROJECT'))


if __name__ == "__main__":
    main()
