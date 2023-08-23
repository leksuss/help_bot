# Help bot

This is a couple of simple bots working in [VK](https://vk.com/) and [Telegram](https://telegram.org/). It is made for answer on ordinary questions from users of some company. Bots are using [DialogFlow Google AI service](https://dialogflow.cloud.google.com/). That means bots can understand different phorms of one phrase. Look at this magic:
<p align="center"><img src="https://github.com/leksuss/help_bot/blob/main/.github/tg_bot_example.gif"></p>

And of course you can try this conversation yourself, here is links to working bots:
 - [VK bot](https://vk.com/im?sel=-219218073)
 - [TG bot](https://t.me/sstorage_bot)

## Requirements

 - python3.6+
 - `python-telegram-bot`
 - `environs`
 - `google-cloud-dialogflow`
 - `google-cloud-api-keys`
 - `vk_api`
 - `requests`

## How to setup

Bot interacts with VK, Telegram and DialogFlow Google service. So, you need to get access from all this services:

 - Receive `credentials.json` file and DialogFlow project id. Go [here](https://cloud.google.com/dialogflow/es/docs/quick/setup) and follow instructions;
 - [create telegram bot](https://core.telegram.org/bots#how-do-i-create-a-bot) and receive token;
 - [create VK group](https://vk.com/groups?tab=admin), receive token and allow community to receive messages from users.
 - (OPTIONAL) create second telegram bot to receive bots logs and write [@userinfobot](https://t.me/userinfobot) to get your chat_id to fill `ADMIN_TG_CHAT_ID`

Use above information for fill settings in `.env` file. You can use `.env_example` as a template. Here is short description of each param:
```
TG_TOKEN - telegram help bot token
VK_TOKEN - vk help bot token
GOOGLE_APPLICATION_CREDENTIALS - path to file credentials.json
GOOGLE_CLOUD_PROJECT - dialogflow project id
TG_LOGBOT_TOKEN - optional, telegram log bot token (for logs)
ADMIN_TG_CHAT_ID - optional, telegram admin chat id (for logs)
```

## How to upload questions and answer in DialogFlow service to teach AI

First you need to get access to DialogFlow API as wrote above. Next, you should create JSON file with structure like this:
```json
{
    "Устройство на работу": {
        "questions": [
            "Как устроиться к вам на работу?",
            "Как устроиться к вам?",
            "Как работать у вас?",
            "Хочу работать у вас",
            "Возможно-ли устроиться к вам?",
            "Можно-ли мне поработать у вас?",
            "Хочу работать редактором у вас"
        ],
        "answer": "Если вы хотите устроиться к нам, напишите на почту game-of-verbs@gmail.com мини-эссе о себе и прикрепите ваше портфолио."
    }
}
```

And then run `create_intent.py` script passing this file as a parameter:
```python
python3 create_intent.py file.json
```


### How to run

Get the source code of this repo:
```bash
git clone git@github.com:leksuss/help_bot.git
```

Go inside folder:
```bash
cd help_bot
```

Python3 should be already installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:
```bash
# If you would like to install dependencies inside virtual environment, you should create it first.
pip3 install -r requirements.txt
```

And then run both bots, each in separate console:
```python
python3 tg_bot.py
```
and
```python
python3 vk_bot.py
```

## Goals
This project is made for study purpose.
