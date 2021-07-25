def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="BOT WSS NO AR\n VAMO TIMEEE"
    )


def echo(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text
    )


def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text='não sei o que fazer com esse comando, mestre'
    )
