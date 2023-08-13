from environs import Env
import logging

from google.cloud import api_keys_v2
from google.cloud.api_keys_v2 import Key
from google.cloud import dialogflow

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

USER_SESSIONS = {}

def start(update, _):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте, {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update, _):
    update.message.reply_text('Help!')


def reply(update, _, google_project_id):
    session_client, session = get_dialogflow_sessions(
        google_project_id, update.effective_user.id
    )
    text_input = dialogflow.TextInput(text=update.message.text, language_code='ru-RU')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    update.message.reply_text(response.query_result.fulfillment_text)


def setup_tg_bot(tg_token, google_project_id):
    updater = Updater(tg_token, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help_command))
    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.text & ~Filters.command,
            lambda update, context: reply(update, context, google_project_id)
        )
    )

    updater.start_polling()
    updater.idle()


def get_dialogflow_sessions(project_id, session_id):
    session_client = dialogflow.SessionsClient()
    if session_id not in USER_SESSIONS:
        USER_SESSIONS[session_id] = session_client.session_path(project_id, session_id)
    return session_client, USER_SESSIONS[session_id]



def main() -> None:
    env = Env()
    env.read_env()

    setup_tg_bot(env('TG_TOKEN'), env('GOOGLE_CLOUD_PROJECT'))



if __name__ == '__main__':
    main()
