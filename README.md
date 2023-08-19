# Help bot

This is a couple of simple bots working in [VK](https://vk.com/) and [Telegram](https://telegram.org/). It is made for answer on ordinary questions from users of some company. Bots are using [DialogFlow Google AI service](https://dialogflow.cloud.google.com/). That means bots can understand different phorms of one phrase.
Here is a working examples:
 - 

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

 - To get it you need to things: `credentials.json` file and DialogFlow project id.
Go [here](https://cloud.google.com/dialogflow/es/docs/quick/setup) and follow instructions;
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

### How to run

Get the source code of this repo:
```
git clone git@github.com:leksuss/help_bot.git
```

Go inside folder:
```
cd help_bot
```

Python3 should be already installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:
```
# If you would like to install dependencies inside virtual environment, you should create it first.
pip3 install -r requirements.txt
```

And then run both bots, each in separate console:
```
python3 tg_bot.py
```
and
```
python3 vk_bot.py
```

## Goals
This project is made for study purpose.
