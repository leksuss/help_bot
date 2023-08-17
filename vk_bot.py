import logging
import random

from environs import Env
from google.cloud import dialogflow
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

USER_SESSIONS = {}


def send_reply(event, vk_api, google_project_id):
    session_client, session = get_dialogflow_sessions(
        google_project_id, event.user_id
    )
    text_input = dialogflow.TextInput(text=event.text, language_code='ru-RU')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    vk_api.messages.send(
        user_id=event.user_id,
        message=response.query_result.fulfillment_text,
        random_id=random.randint(1,1000),
    )


def get_dialogflow_sessions(project_id, session_id):
    session_client = dialogflow.SessionsClient()
    if session_id not in USER_SESSIONS:
        USER_SESSIONS[session_id] = session_client.session_path(project_id, session_id)
    return session_client, USER_SESSIONS[session_id]


def main():
    env = Env()
    env.read_env()

    vk_session = vk.VkApi(token=env('VK_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_reply(event, vk_api, env('GOOGLE_CLOUD_PROJECT'))


if __name__ == "__main__":
    main()
