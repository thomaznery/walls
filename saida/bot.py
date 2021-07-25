import json
from telegram import Bot, Update
from telegram.ext import CommandHandler, Dispatcher, Filters, MessageHandler
from handlers import echo, start, unknown
import boto3
from botocore.vendored import requests  # necesario para a AWS

ssm_client = boto3.client("ssm", region_name='sa-east-1')
response = ssm_client.get_parameter(Name="telegram-token", WithDecryption=True)
TELEGRAM_TOKEN = response["Parameter"]["Value"]
bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot, None, use_context=True)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))


def lambda_handler(event, context):
    dispatcher.process_update(Update.de_json(json.loads(event["body"]), bot))
    return {"statusCode": 200}
