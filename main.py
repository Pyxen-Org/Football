from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(f"Hello {user.first_name}! This is your basic Telegram bot ⚽")

def main():
    TOKEN = "8301290642:AAEUw6oa1C1fLIXPBpqRiIJjOYFhrG5sLco"  # Replace with your bot token
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
