import logging
from google.cloud import dialogflow


logger = logging.getLogger(__name__)


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=[message_texts])
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )
    logger.info(f'Intent created: {response}')



def get_dialogflow_answer(user_id, user_text, project_id, is_fallback=False):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, user_id)

    text_input = dialogflow.TextInput(text=user_text, language_code='ru-RU')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={'session': session, 'query_input': query_input}
    )
    if is_fallback and response.query_result.intent.is_fallback:
        return None
    return response.query_result.fulfillment_text
