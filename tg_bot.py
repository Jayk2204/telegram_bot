from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import logging

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

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome! Please enter your name:")
    return

def get_name(update: Update, context: CallbackContext) -> None:
    user_name = update.message.text
    user_id = update.message.chat_id
    user_data[user_id] = {"name": user_name}
    
    keyboard = [
        [InlineKeyboardButton("Assignments 📚", callback_data='assignments')],
        [InlineKeyboardButton("Practical Assignments 📝", callback_data='practicals')],
        [InlineKeyboardButton("IMPs 🔥", callback_data='imps')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f"Hello {user_name}, what do you need?", reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    if query.data in ["assignments", "practicals", "imps"]:
        keyboard = [[InlineKeyboardButton(subject, callback_data=subject)] for subject in pdf_links.keys()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Select a subject:", reply_markup=reply_markup)
    
    elif query.data in pdf_links:
        pdf_buttons = [
            [InlineKeyboardButton(f"Download {i+1}", url=pdf)]
            for i, pdf in enumerate(pdf_links[query.data])
        ]
        reply_markup = InlineKeyboardMarkup(pdf_buttons)
        query.edit_message_text(f"Here are the PDFs for {query.data}:", reply_markup=reply_markup)

def main():
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_name))
    dp.add_handler(CallbackQueryHandler(button))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
