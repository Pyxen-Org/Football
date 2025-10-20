from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import html
import asyncio

# Features import
from feedback import add_feedback_handlers
from db import create_game, set_host, get_game, init_db

# ======================
# /start COMMAND
# ======================
def start(update: Update, context: CallbackContext):
    welcome_text = (
        "⚽ 𝐖ᴇʟᴄᴏᴍᴇ Tᴏ Fᴏᴏᴛʙᴀʟʟ Bᴏᴛ!\n\n"
        "🎮 Sᴛᴇᴘ ᴏɴᴛᴏ ᴛʜᴇ ᴠɪʀᴛᴜᴀʟ ᴘɪᴛᴄʜ, sᴛʀᴀᴛᴇɢɪᴢᴇ, ʙᴜɪʟᴅ ʏᴏᴜʀ ᴛᴇᴀᴍ, ᴀɴᴅ ᴘʟᴀʏ ᴊᴜsᴛ ʟɪᴋᴇ ɪɴ ᴀ ʀᴇᴀʟ ғᴏᴏᴛʙᴀʟʟ ᴍᴀᴛᴄʜ!\n\n"
        "🔥 Fʀᴇᴇ ᴛʜᴇ ᴀᴅʀᴇɴᴀʟɪɴᴇ ʀᴜsʜ ᴀs ʏᴏᴜ sᴄᴏʀᴇ ɢᴏᴀʟs, ᴍᴀᴋᴇ sᴍᴀʀᴛ ᴘʟᴀʏs, ᴀɴᴅ ʀɪsᴇ ᴛᴏ ᴛʜᴇ ᴛᴏᴘ ᴏғ ᴛʜᴇ ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ.\n"
        "🏆 Tʀᴀɪɴ - Cᴏᴍᴘᴇᴛᴇ - Cᴏɴǫᴜᴇʀ\n\n"
        "Tʏᴘᴇ /help ᴛᴏ ʟᴇᴀʀɴ ʜᴏᴡ ᴛᴏ ɢᴇᴛ sᴛᴀʀᴛᴇᴅ ᴀɴᴅ ᴍᴀsᴛᴇʀ ᴛʜᴇ ɢᴀᴍᴇ!"
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
        "- /newgame: to start the game.\n"
        "- /feedback: share your feedback to log/support group."
    )
    keyboard = [[InlineKeyboardButton("Alright!", callback_data="delete_help")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(help_text, reply_markup=reply_markup)


# ======================
# /rules COMMAND
# ======================
def rules_command(update: Update, context: CallbackContext):
    rules_text = "📜 Game Rules:\n\n1️⃣ Be fair.\n2️⃣ Respect others.\n3️⃣ No spam.\n4️⃣ Have fun!"
    keyboard = [[InlineKeyboardButton("🎐 I Understood!", callback_data="delete_rules")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(rules_text, reply_markup=reply_markup)


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
async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    chat = query.message.chat

    # DELETE HELP BUTTON
    if query.data == "delete_help":
        await query.message.delete()

    # DELETE RULES BUTTON
    elif query.data == "delete_rules":
        await query.message.delete()

    # BECOME HOST BUTTON
    elif query.data == "become_host":
        member = await chat.get_member(user.id)
        if member.status in ["administrator", "creator"]:
            safe_name = html.escape(user.first_name)
            await create_game(chat.id, user.id, safe_name)
            new_text = f"🎉 <a href='tg://user?id={user.id}'>{safe_name}</a> is now the game host! Create teams by using /create_teams. Let's get the match started"
            try:
                await query.message.edit_text(new_text, parse_mode="HTML", reply_markup=None)
            except:
                pass
            await query.answer("✅ You are now the game host!", show_alert=True)
        else:
            await query.answer("❌ You are not an admin! Ask a group admin to host.", show_alert=True)


# ======================
# MAIN FUNCTION
# ======================
def main():
    TOKEN = "8301290642:AAEUw6oa1C1fLIXPBpqRiIJjOYFhrG5sLco"
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Initialize DB pool
    asyncio.run(init_db())

    # Add handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("rules", rules_command))
    dp.add_handler(CommandHandler("newgame", newgame_command))

    # External Db import
    add_feedback_handlers(dp)
    dp.add_handler(CallbackQueryHandler(button_callback))  # single callback for all buttons

    print("⚽ Bot is running...")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
