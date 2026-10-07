import os
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
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


# =========================
# MAIN MENU
# =========================

def main_menu():
    keyboard = [
        [
            InlineKeyboardButton(
                "📢 Sports Updates",
                callback_data="sports"
            )
        ],
        [
            InlineKeyboardButton(
                "🌐 Website",
                callback_data="website"
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ️ About Us",
                callback_data="about"
            )
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# START COMMAND
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    welcome_text = """
<b>Welcome To G168-SPORT</b>

សូមស្វាគមន៍មកកាន់ G168-SPORT!

ទទួលបានព័ត៌មានកីឡា ព័ត៌មានបាល់ទាត់
លទ្ធផល និងព័ត៌មានថ្មីៗនៅទីនេះ។

សូមជ្រើសរើសជម្រើសខាងក្រោម 👇
"""

    if os.path.exists(IMAGE_PATH):

        try:
            with open(IMAGE_PATH, "rb") as photo:

                await update.message.reply_photo(
                    photo=photo,
                    caption=welcome_text,
                    parse_mode="HTML",
                    reply_markup=main_menu()
                )

        except Exception as error:

            logger.error("Could not send image: %s", error)

            await update.message.reply_text(
                welcome_text,
                parse_mode="HTML",
                reply_markup=main_menu()
            )

    else:

        logger.error("IMAGE NOT FOUND: %s", IMAGE_PATH)

        await update.message.reply_text(
            welcome_text,
            parse_mode="HTML",
            reply_markup=main_menu()
        )


# =========================
# BUTTON RESPONSES
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    # SPORTS UPDATES
    if query.data == "sports":

        text = """
<b>📢 Sports Updates</b>

Welcome to G168-SPORT.

Here you can receive the latest sports information,
football news, match updates and other sports content.

Please check back for new updates.
"""

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔙 Back to Menu",
                    callback_data="menu"
                )
            ]
        ]

        await query.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # WEBSITE
    elif query.data == "website":

        text = """
<b>🌐 Website</b>

Visit our official website below:

https://example.com

Tap the link above to visit the website.
"""

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔙 Back to Menu",
                    callback_data="menu"
                )
            ]
        ]

        await query.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # ABOUT US
    elif query.data == "about":

        text = """
<b>ℹ️ About G168-SPORT</b>

G168-SPORT provides sports information,
football news, match updates and other
sports-related content.

Thank you for using our Telegram bot. ⚽
"""

        keyboard = [
            [
                InlineKeyboardButton(
                    "🔙 Back to Menu",
                    callback_data="menu"
                )
            ]
        ]

        await query.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


    # BACK TO MENU
    elif query.data == "menu":

        text = """
<b>🏠 Main Menu</b>

Please choose an option below 👇
"""

        await query.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=main_menu()
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
# START BOT
# =========================

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

    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    application.add_error_handler(
        error_handler
    )

    print("Bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()
