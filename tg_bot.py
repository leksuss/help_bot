import logging

from environs import Env
from telegram import ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from dialogflow_api import get_dialogflow_answer
from log_handler import TelegramLogsHandler


logger = logging.getLogger(__name__)


def start(update, _):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте, {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )
    logger.info(f'User {update.effective_user.id} push start')


def send_reply(update, project_id):
    try:
        query_result = get_dialogflow_answer(
            update.effective_user.id,
            update.message.text,
            project_id,
        )
        update.message.reply_text(query_result.fulfillment_text)
    except Exception as e:
        logger.exception(e)


def main() -> None:
    env = Env()
    env.read_env()

    if env('TG_LOGBOT_TOKEN', None) and env('ADMIN_TG_CHAT_ID', None):
        handler = TelegramLogsHandler(env('TG_LOGBOT_TOKEN'), env('ADMIN_TG_CHAT_ID'))
    else:
        handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    updater = Updater(env('TG_TOKEN'))
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.text & ~Filters.command,
            lambda update, _: send_reply(update, env('GOOGLE_CLOUD_PROJECT'))
        )
    )

    logger.info(f'Bot tg_bot started')

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
