from environs import Env
import json

from dialogflow_api import create_intent


if __name__ == '__main__':
    file_url = 'questions.json'
    env = Env()
    env.read_env()

    with open(file_url, 'r') as f:
        questions = json.load(f)

    for title, q_and_a in questions.items():
        create_intent(
            env('GOOGLE_CLOUD_PROJECT'),
            title,
            q_and_a['questions'],
            q_and_a['answer'],
        )
