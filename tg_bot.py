from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext

import logging

# Enable logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Dictionary to store user details
user_data = {}

# Dictionary containing subjects and PDF links
pdf_links = {
    "SAM": ["https://yourserver.com/samAssignment1.pdf", "https://yourserver.com/samAssignment2.pdf"],
    "CN": ["https://drive.google.com/file/d/1-7dMn15nM_sAGYy3xDWnRofYPDorDER1/view?usp=sharing", "https://yourserver.com/cnAssignment2.pdf"],
    "AI": ["https://drive.google.com/file/d/1-9NJzS-Rzm3T7U7X85MEOJ6VfTFiKIO_/view?usp=sharing"],
    "SEO": ["https://drive.google.com/file/d/1-HTKJHmHy56RV4_S1w-rTYhVoLEvMyeu/view?usp=drive_link"],
    "WordPress": ["https://yourserver.com/wpAssignment1.pdf"]
}

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Welcome! Please enter your name:")

async def get_name(update: Update, context: CallbackContext) -> None:
    user_name = update.message.text
    user_id = update.message.chat_id
    user_data[user_id] = {"name": user_name}
    
    keyboard = [
        [InlineKeyboardButton("Assignments 📚", callback_data='assignments')],
        [InlineKeyboardButton("Practical Assignments 📝", callback_data='practicals')],
        [InlineKeyboardButton("IMPs 🔥", callback_data='imps')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"Hello {user_name}, what do you need?", reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data in ["assignments", "practicals", "imps"]:
        keyboard = [[InlineKeyboardButton(subject, callback_data=subject)] for subject in pdf_links.keys()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Select a subject:", reply_markup=reply_markup)
    
    elif query.data in pdf_links:
        pdf_buttons = [
            [InlineKeyboardButton(f"Download {i+1}", url=pdf)]
            for i, pdf in enumerate(pdf_links[query.data])
        ]
        reply_markup = InlineKeyboardMarkup(pdf_buttons)
        await query.edit_message_text(f"Here are the PDFs for {query.data}:", reply_markup=reply_markup)

async def main():
    app = Application.builder().token("8088841239:AAHgw4Zgyt8FOdpaFX7TJKLfaejN8IG2vi8").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_name))
    app.add_handler(CallbackQueryHandler(button))

    logger.info("Bot is running...")
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
