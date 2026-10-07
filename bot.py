import os
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

# =========================
# SETTINGS
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")

IMAGE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "images",
    "welcome.jpg"
)

# =========================
# LOGGING
# =========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


# =========================
# START COMMAND
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    welcome_text = """
<b>Welcome To 855GOAL</b>

សូមស្វាគមន៍មកកាន់ 855GOAL!

ទទួលបានព័ត៌មានកីឡា ព័ត៌មានបាល់ទាត់
លទ្ធផល និងព័ត៌មានថ្មីៗនៅទីនេះ។

សូមជ្រើសរើសជម្រើសខាងក្រោម 👇
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "📢 Sports Updates",
                url="https://t.me/YOUR_CHANNEL"
            )
        ],
        [
            InlineKeyboardButton(
                "🌐 Website",
                url="https://example.com"
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ️ About Us",
                url="https://example.com/about"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Check whether image exists
    if os.path.exists(IMAGE_PATH):

        with open(IMAGE_PATH, "rb") as photo:

            await update.message.reply_photo(
                photo=photo,
                caption=welcome_text,
                parse_mode="HTML",
                reply_markup=reply_markup
            )

    else:

        # If image is missing, still respond
        logger.error(
            "Image not found: %s",
            IMAGE_PATH
        )

        await update.message.reply_text(
            welcome_text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )


# =========================
# ERROR HANDLER
# =========================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    logger.error(
        "Exception while processing update:",
        exc_info=context.error
    )


# =========================
# MAIN
# =========================

def main():

    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN environment variable is missing."
        )

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_error_handler(error_handler)

    print("Bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()
