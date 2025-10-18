from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from datetime import datetime

# Your log group ID
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

    query.message.reply_text(f"💬 Please type your message for **{category}** below:")
    query.message.delete()  # clean interface


# ======================
# CAPTURE FEEDBACK MESSAGE
# ======================
def feedback_message_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    category = context.user_data.get("feedback_category")

    # If user didn't choose a category first
    if not category:
        update.message.reply_text("⚠️ Please use /feedback first to choose a feedback type.")
        return

    feedback_text = update.message.text
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Send to log group
    feedback_msg = (
        f"🗂 <b>Category:</b> {category}\n"
        f"👤 <b>From:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
        f"🕒 <b>Time:</b> {timestamp}\n"
        f"💬 <b>Feedback:</b> {feedback_text}"
    )

    context.bot.send_message(
        chat_id=LOG_GROUP_ID,
        text=feedback_msg,
        parse_mode="HTML"
    )

    # Acknowledge user with popup
    update.message.reply_text("✅ Thank you for your feedback! It’s been submitted successfully.")

    # Clean up user_data to reset feedback flow
    context.user_data.pop("feedback_category", None)


# ======================
# HANDLER SETUP FUNCTION
# ======================
def add_feedback_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("feedback", feedback_command))
    dispatcher.add_handler(CallbackQueryHandler(feedback_category_callback, pattern="^feedback_"))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, feedback_message_handler))
