import argparse
import json
import logging

from environs import Env
from dialogflow_api import create_intent


logger = logging.getLogger(__name__)


def read_args():
    parser = argparse.ArgumentParser(
        description='''
            Tool for upload intents in dialogflow service
        '''
    )
    parser.add_argument(
        'intents_file',
        type=argparse.FileType('r'),
        help='JSON file with intents to upload'
    )

    args = parser.parse_args()
    return args


def run():
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(message)s'))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    logger.info('start script')
    args = read_args()
    env = Env()
    env.read_env()
    questions = json.load(args.intents_file)
    logger.info('loaded file')

    for title, q_and_a in questions.items():
        create_intent(
            env('GOOGLE_CLOUD_PROJECT'),
            title,
            q_and_a['questions'],
            q_and_a['answer'],
        )


if __name__ == '__main__':
    run()
