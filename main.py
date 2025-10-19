import asyncio
import html
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)

# Features import
from feedback import add_feedback_handlers
from db import connect_db, create_game, get_game, set_host

# ======================
# /start COMMAND
# ======================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)


# ======================
# /help COMMAND
# ======================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🏟️ Current Commands:\n\n"
        "- /newgame: to start the game.\n"
        "- /feedback: share your feedback to log/support group."
    )
    keyboard = [[InlineKeyboardButton("Alright!", callback_data="delete_help")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(help_text, reply_markup=reply_markup)


# ======================
# /rules COMMAND
# ======================
async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rules_text = "Game Rules:-"
    keyboard = [[InlineKeyboardButton("🎐 I Understood!", callback_data="delete_rules")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(rules_text, reply_markup=reply_markup)


# ======================
# /newgame COMMAND
# ======================
async def newgame_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_type = update.effective_chat.type
    if chat_type == "private":
        await update.message.reply_text("⚠️ Use /newgame in a group to start a game!")
        return

    chat_id = update.effective_chat.id
    conn = context.bot_data["db"]

    existing_game = await get_game(conn, chat_id)
    if existing_game:
        await update.message.reply_text("A game is already ongoing!")
        return

    game_id = await create_game(conn, chat_id)

    text = "🎉 New Game Alert! 🎉\n\nWho will be the game host for this match? 🤔"
    keyboard = [[InlineKeyboardButton("🎭 I'm the host!", callback_data=f"become_host:{game_id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)


# ======================
# CALLBACK HANDLER
# ======================
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    chat = query.message.chat
    conn = context.bot_data["db"]

    await query.answer()  # required to acknowledge click

    data = query.data

    # Delete messages
    if data in ["delete_help", "delete_rules"]:
        await query.message.delete()
        return

    # Become host
    if data.startswith("become_host:"):
        game_id = int(data.split(":")[1])
        member = await chat.get_member(user.id)
        if member.status in ["administrator", "creator"]:
            await set_host(conn, game_id, user.id)
            safe_name = html.escape(user.first_name)
            new_text = f"🎉 <a href='tg://user?id={user.id}'>{safe_name}</a> is now the game host! Create teams by using /create_teams. Let's get the match started"
            try:
                await query.message.edit_text(new_text, parse_mode="HTML", reply_markup=None)
            except:
                pass
            await query.answer(text="✅ You are now the game host!", show_alert=True)
        else:
            await query.answer(text="❌ You are not an admin! Ask a group admin to host.", show_alert=True)


# ======================
# MAIN FUNCTION
# ======================
async def main():
    TOKEN = "8301290642:AAEUw6oa1C1fLIXPBpqRiIJjOYFhrG5sLco"
    app = ApplicationBuilder().token(TOKEN).build()

    # Connect DB
    app.bot_data["db"] = await connect_db()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("rules", rules_command))
    app.add_handler(CommandHandler("newgame", newgame_command))
    add_feedback_handlers(app)  # feedback handlers
    app.add_handler(CallbackQueryHandler(button_callback))  # single callback for all buttons

    print("⚽ Bot is running...")
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
