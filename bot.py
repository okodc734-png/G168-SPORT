import os
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

IMAGE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "5922410746572639996.jpg"
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    welcome_text = """
<b>Welcome To G168-SPORT</b>

សូមស្វាគមន៍មកកាន់ G168-SPORT!

ទទួលបានព័ត៌មានកីឡា ព័ត៌មានបាល់ទាត់
លទ្ធផល និងព័ត៌មានថ្មីៗនៅទីនេះ។

សូមជ្រើសរើសជម្រើសខាងក្រោម 👇
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "📢 CHANNEL UPDATE",
                url="https://t.me/Game855GOAL"
            )
        ],
        [
            InlineKeyboardButton(
                "🌐 WEBSITE",
                url="https://heylink.me/855goal/"
            )
        ],
        [
            InlineKeyboardButton(
                "💬 DM NOW",
                url="https://t.me/GOALWIN855"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if os.path.exists(IMAGE_PATH):

        try:
            with open(IMAGE_PATH, "rb") as photo:
                await update.message.reply_photo(
                    photo=photo,
                    caption=welcome_text,
                    parse_mode="HTML",
                    reply_markup=reply_markup
                )

        except Exception as error:
            logger.error("Could not send image: %s", error)

            await update.message.reply_text(
                welcome_text,
                parse_mode="HTML",
                reply_markup=reply_markup
            )

    else:
        logger.error("IMAGE NOT FOUND: %s", IMAGE_PATH)

        await update.message.reply_text(
            welcome_text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):
    logger.error(
        "Exception while processing update:",
        exc_info=context.error
    )


def main():

    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN environment variable is missing. "
            "Add BOT_TOKEN in Railway Variables."
        )

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_error_handler(
        error_handler
    )

    print("Bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()
