from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# ======================
# /start COMMAND
# ======================
def start(update: Update, context: CallbackContext):
    # Welcome message
    welcome_text = (
        "⚽ 𝐖ᴇʟᴄᴏᴍᴇ Tᴏ Fᴏᴏᴛʙᴀʟʟ Bᴏᴛ!\n\n"
        "🎮 Sᴛᴇᴘ ᴏɴᴛᴏ ᴛʜᴇ ᴠɪʀᴛᴜᴀʟ ᴘɪᴛᴄʜ, sᴛʀᴀᴛᴇɢɪᴢᴇ, ʙᴜɪʟᴅ ʏᴏᴜʀ ᴛᴇᴀᴍ, ᴀɴᴅ ᴘʟᴀʏ ᴊᴜsᴛ ʟɪᴋᴇ ɪɴ ᴀ ʀᴇᴀʟ ғᴏᴏᴛʙᴀʟʟ ᴍᴀᴛᴄʜ!\n\n"
        "🔥 Fʀᴇᴇ ᴛʜᴇ ᴀᴅʀᴇɴᴀʟɪɴᴇ ʀᴜsʜ ᴀs ʏᴏᴜ sᴄᴏʀᴇ ɢᴏᴀʟs, ᴍᴀᴋᴇ sᴍᴀʀᴛ ᴘʟᴀʏs, ᴀɴᴅ ʀɪsᴇ ᴛᴏ ᴛʜᴇ ᴛᴏᴘ ᴏғ ᴛʜᴇ ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ.\n"
        "🏆 Tʀᴀɪɴ - Cᴏᴍᴘᴇᴛᴇ - Cᴏɴǫᴜᴇʀ\n\n"
        "Tʏᴘᴇ /help ᴛᴏ ʟᴇᴀʀɴ ʜᴏᴡ ᴛᴏ ɢᴇᴛ sᴛᴀʀᴛᴇᴅ ᴀɴᴅ ᴍᴀsᴛᴇʀ ᴛʜᴇ ɢᴀᴍᴇ!"
    )

    # Inline buttons
    keyboard = [
        [
            InlineKeyboardButton("Support", url="https://t.me/YOUR_SUPPORT_LINK"),
            InlineKeyboardButton("Updates", url="https://t.me/YOUR_UPDATES_CHANNEL")
        ],
        [
            InlineKeyboardButton("Add bot to your group", url="https://t.me/footballbeta_bot?startgroup=true")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(welcome_text, reply_markup=reply_markup)


# ======================
# /help COMMAND
# ======================
def help_command(update: Update, context: CallbackContext):
    help_text = (
        "🏟️ Current Commands:\n\n"
        "1️⃣ Press /newgame to start the game."
    )

    # Inline button to delete the message
    keyboard = [
        [InlineKeyboardButton("Alright!", callback_data="delete_help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(help_text, reply_markup=reply_markup)

# ======================
# CALLBACK HANDLER
# ======================
def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()  # Acknowledge the button click
    if query.data == "delete_help":
        query.message.delete()  # Delete the help message


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackQueryHandler, CallbackContext

# ======================
# /newgame COMMAND
# ======================
def newgame_command(update: Update, context: CallbackContext):
    text = "🎉 New Game Alert! 🎉\n\nWho will be the game host for this match? 🤔"

    # Inline button to become the host
    keyboard = [
        [InlineKeyboardButton("Im tha host", callback_data="become_host")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(text, reply_markup=reply_markup)

# ======================
# CALLBACK HANDLER
# ======================
def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()  # acknowledge button click

    if query.data == "delete_help":
        query.message.delete()

    elif query.data == "become_host":
        # Show a new message confirming host
        keyboard = [[InlineKeyboardButton("OK", callback_data="ok_host")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("✅ You are the host!", reply_markup=reply_markup)

    elif query.data == "ok_host":
        # Just acknowledge or optionally delete the message
        query.message.delete()

# ======================
# MAIN FUNCTION
# ======================
def main():
    TOKEN = "8301290642:AAEUw6oa1C1fLIXPBpqRiIJjOYFhrG5sLco"  # Replace with your bot token
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add /start handler
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CallbackQueryHandler(button_callback))
    dp.add_handler(CommandHandler("newgame", newgame_command))
dp.add_handler(CallbackQueryHandler(button_callback))  # Already handles previous buttons too

# Start the bot
updater.start_polling()
updater.idle()

if __name__ == "__main__":
    main()
