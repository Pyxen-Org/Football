from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from db import connect_db, create_game, get_game, set_host
import asyncio


# ======================
# /start COMMAND
# ======================
def start(update: Update, context: CallbackContext):
    welcome_text = (
        "⚽ 𝐖ᴇʟᴄᴏᴍᴇ Tᴏ Fᴏᴏᴛʙᴀʟʟ Bᴏᴛ!\n\n"
        "🎮 Step onto the virtual pitch, strategize, build your team, and play like it’s a real match!\n\n"
        "🔥 Score goals, make smart plays, and rise to the leaderboard.\n"
        "🏆 Train - Compete - Conquer\n\n"
        "Type /help to learn how to get started!"
    )

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
        "1️⃣ /newgame — Start a new match.\n"
        "2️⃣ /feedback — Send your feedback."
    )
    keyboard = [[InlineKeyboardButton("Alright!", callback_data="delete_help")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(help_text, reply_markup=reply_markup)


# ======================
# /newgame COMMAND
# ======================
def newgame_command(update: Update, context: CallbackContext):
    chat_type = update.effective_chat.type
    if chat_type == "private":
        update.message.reply_text("⚠️ Use /newgame in a group to start a game!")
        return

    text = "🎉 New Game Alert! 🎉\n\nWho will be the game host for this match? 🤔"
    keyboard = [[InlineKeyboardButton("🎭 I'm the host!", callback_data="become_host")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text, reply_markup=reply_markup)


# ======================
# CALLBACK HANDLER
# ======================
def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    chat = query.message.chat
    query.answer()

    if query.data == "delete_help":
        query.message.delete()

    elif query.data == "become_host":
        member = chat.get_member(user.id)
        if member.status in ["administrator", "creator"]:
            new_text = f"🎉 [{user.first_name}](tg://user?id={user.id}) is now the game host! Let's get started!"
            query.message.edit_text(new_text, parse_mode="Markdown")
            query.answer("✅ You are now the game host!", show_alert=True)
        else:
            query.answer("❌ You are not an admin! Ask a group admin to host.", show_alert=True)


# ======================
# MAIN FUNCTION
# ======================
def main():
    TOKEN = "YOUR_BOT_TOKEN_HERE"
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Register commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("newgame", newgame_command))
    dp.add_handler(CallbackQueryHandler(button_callback))

    print("⚽ Bot is running...")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
