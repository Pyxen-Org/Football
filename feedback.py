from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from datetime import datetime
import html

LOG_GROUP_ID = -1003133644267

# ======================
# /feedback COMMAND
# ======================
def feedback_command(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("🏗 Feature Request", callback_data="feedback_feature"),
            InlineKeyboardButton("🐞 Bug Report", callback_data="feedback_bug")
        ],
        [
            InlineKeyboardButton("💭 Suggestion", callback_data="feedback_suggestion"),
            InlineKeyboardButton("❤️ Appreciation", callback_data="feedback_appreciation")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "🧠 What type of feedback would you like to share?",
        reply_markup=reply_markup
    )


# ======================
# CATEGORY SELECTION
# ======================
def feedback_category_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    category_map = {
        "feedback_feature": "Feature Request",
        "feedback_bug": "Bug Report",
        "feedback_suggestion": "Suggestion",
        "feedback_appreciation": "Appreciation"
    }

    category = category_map.get(query.data)
    context.user_data["feedback_category"] = category

    # Delete the button message
    try:
        query.message.delete()
    except:
        pass

    query.message.reply_text(f"💬 Please type your message for *{category}* below:", parse_mode="Markdown")


# ======================
# CAPTURE FEEDBACK MESSAGE
# ======================
def feedback_message_handler(update, context):
    user = update.effective_user
    msg = update.effective_message

    # Only proceed if user has selected feedback category
    category = context.user_data.get("feedback_category")
    if not category:
        return  # ignore message, don’t reply

    # Now handle feedback normally
    feedback_text = msg.text
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    escaped_feedback = html.escape(feedback_text)
    escaped_name = html.escape(user.first_name)

    feedback_msg = (
        f"🗂 <b>Category:</b> {category}\n"
        f"👤 <b>From:</b> <a href='tg://user?id={user.id}'>{escaped_name}</a>\n"
        f"🕒 <b>Time:</b> {timestamp}\n"
        f"💬 <b>Feedback:</b> {escaped_feedback}"
    )

    context.bot.send_message(
        chat_id=LOG_GROUP_ID,
        text=feedback_msg,
        parse_mode="HTML"
    )

    msg.reply_text("✅ Thank you for your feedback! It’s been submitted successfully.")
    context.user_data.pop("feedback_category", None)

# ======================
# REGISTER HANDLERS
# ======================
def add_feedback_handlers(dispatcher):
    # feedback handlers must come BEFORE the main callback handler
    dispatcher.add_handler(CommandHandler("feedback", feedback_command))
    dispatcher.add_handler(CallbackQueryHandler(feedback_category_callback, pattern="^feedback_"))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, feedback_message_handler))
