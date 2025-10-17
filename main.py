from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext

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
# MAIN FUNCTION
# ======================
def main():
    TOKEN = "8301290642:AAEUw6oa1C1fLIXPBpqRiIJjOYFhrG5sLco"  # Replace with your bot token
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add /start handler
    dp.add_handler(CommandHandler("start", start))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
