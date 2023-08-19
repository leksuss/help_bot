import logging

from environs import Env
from telegram import ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from dialogflow_api import get_dialogflow_answer


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def start(update, _):
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуйте, {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )
    logger.info(f'User {update.effective_user.id} push start')


def send_reply(update, project_id):
    reply = get_dialogflow_answer(
        update.effective_user.id,
        update.message.text,
        project_id,
    )
    update.message.reply_text(reply)


def main() -> None:
    env = Env()
    env.read_env()

    updater = Updater(env('TG_TOKEN'))
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.text & ~Filters.command,
            lambda update, context: send_reply(update, env('GOOGLE_CLOUD_PROJECT'))
        )
    )

    updater.start_polling()
    updater.idle()
    logger.info('Bot tg_bot started')


if __name__ == '__main__':
    main()
