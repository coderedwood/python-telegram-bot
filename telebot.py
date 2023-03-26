import os
from dotenv import load_dotenv
from telegram import *
from telegram.ext import *
import openai

load_dotenv()

print("Starting Bot")
apitoken = os.getenv("GPT_KEY")
openai.api_key = os.getenv("OAI_KEY")


# Define a functions to handle incoming messages

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    await update.message.reply_text("Hello there! How goes thee?")

async def help_command(update, context: ContextTypes.DEFAULT_TYPE)-> None:
    await update.message.reply_text("Help message")

async def prompt_command(update, context: ContextTypes.DEFAULT_TYPE)->None:
    prompt = update.message.text
    response = openai.Completion.create(
        model="text-davinci-003", prompt=prompt, temperature=1, max_tokens=200)
    bot_response = response.choices[0].text.strip()
    print(response)
    await update.message.reply_text(bot_response)

def handle_response(text: str) -> str:
    if 'hello' in text:
        return 'Hey there'
    if 'how are you' in text:
        return "I am good, thanks!"

    return 'idk'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    response = ''

    if message_type == 'group':
        if '@MT5Signalsbot' in text:
            new_text = text.replace('MT5Signalsbot', '').strip()
            response = handle_response(new_text)
    else:
        response = handle_response(text)

    await update.message.reply_text(response)


def error(update: Update, context: ContextTypes.DEFAULT_TYPE)-> None:
    print(f'Update {update} caused error:n{context.error}')

if __name__ == '__main__':
    # updater = Updater(apitoken, queue.Queue())
    dp = Application.builder().token(apitoken).build()


    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('prompt', prompt_command))

    # Messages
    dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors
    dp.add_error_handler(error)

    # Run bot
    dp.run_polling()