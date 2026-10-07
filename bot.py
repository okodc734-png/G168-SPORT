import os
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)


# =========================================================
# BOT SETTINGS
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

# The image is in the same folder as bot.py on GitHub
IMAGE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "5922410746572639996.jpg"
)


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


# =========================================================
# /START COMMAND
# =========================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    welcome_text = """
<b>Welcome To G168-SPORT</b>

សូមស្វាគមន៍មកកាន់ G168-SPORT!

ទទួលបានព័ត៌មានកីឡា ព័ត៌មានបាល់ទាត់
លទ្ធផល និងព័ត៌មានថ្មីៗនៅទីនេះ។

សូមជ្រើសរើសជម្រើសខាងក្រោម 👇
"""

    # =====================================================
    # BUTTONS
    # =====================================================

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


    # =====================================================
    # SEND IMAGE + MESSAGE
    # =====================================================

    if os.path.exists(IMAGE_PATH):

        try:

            with open(IMAGE_PATH, "rb") as photo:

                await update.message.reply_photo(
                    photo=photo,
                    caption=welcome_text,
                    parse_mode="HTML",
                    reply_markup=reply_markup
                )

            logger.info("Welcome message and image sent successfully.")

        except Exception as error:

            logger.error(
                "Could not send image: %s",
                error
            )

            # Send text if image sending fails
            await update.message.reply_text(
                welcome_text,
                parse_mode="HTML",
                reply_markup=reply_markup
            )

    else:

        logger.error(
            "IMAGE NOT FOUND: %s",
            IMAGE_PATH
        )

        # The bot will still respond even if the image is missing
        await update.message.reply_text(
            welcome_text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )


# =========================================================
# ERROR HANDLER
# =========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    logger.error(
        "Exception while processing update:",
        exc_info=context.error
    )


# =========================================================
# MAIN BOT
# =========================================================

def main():

    # Check BOT_TOKEN
    if not BOT_TOKEN:

        raise ValueError(
            "BOT_TOKEN environment variable is missing. "
            "Add BOT_TOKEN in Railway Variables."
        )


    # Create Telegram application
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )


    # Register /start command
    application.add_handler(
        CommandHandler("start", start)
    )


    # Register error handler
    application.add_error_handler(
        error_handler
    )


    # Start bot
    print("Bot is running...")

    application.run_polling()


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    main()
