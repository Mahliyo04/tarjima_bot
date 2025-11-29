import logging
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from deep_translator import GoogleTranslator
from gtts import gTTS

logging.basicConfig(level=logging.INFO)

TOKEN = "8236290251:AAGcE5m2kFZ9oClYR6R0PdRPz54sSTK3bGI"
user_mode = {}


# =====================================
# START
# =====================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["🇺🇿 Uzbek → 🇹🇷 Turk"],
        ["🇹🇷 Turk → 🇺🇿 Uzbek"],
        ["❌ Chiqish"]
    ]
    reply_kb = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Tilni tanlang:",
        reply_markup=reply_kb
    )


# =====================================
# TEXT HANDLER
# =====================================
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    # Tugmalarni bosganda rejimni almashtirish
    if text == "🇺🇿 Uzbek → 🇹🇷 Turk":
        user_mode[user_id] = "uz_tr"
        await update.message.reply_text("🇺🇿 Matn yuboring:")
        return

    elif text == "🇹🇷 Turk → 🇺🇿 Uzbek":
        user_mode[user_id] = "tr_uz"
        await update.message.reply_text("🇹🇷 Matn yuboring:")
        return

    elif text == "❌ Chiqish":
        user_mode.pop(user_id, None)
        await update.message.reply_text("Rejim tugatildi. /start bosing.")
        return

    # Avval rejim tanlanishi kerak
    if user_id not in user_mode:
        await update.message.reply_text("Avval tilni tanlang. /start")
        return

    mode = user_mode[user_id]

    # Uzbek → Turk
    if mode == "uz_tr":
        translated = GoogleTranslator(source="uz", target="tr").translate(text)

        voice_file = "tr.mp3"
        gTTS(translated, lang="tr").save(voice_file)

    # Turk → Uzbek
    elif mode == "tr_uz":
        translated = GoogleTranslator(source="tr", target="uz").translate(text)

        voice_file = "tr.mp3"
        gTTS(text, lang="tr").save(voice_file)

    # Tarjima matn
    await update.message.reply_text(f"Tarjima:\n\n{translated}")

    # Ovoz
    await update.message.reply_voice(voice=open(voice_file, "rb"))

    os.remove(voice_file)


# =====================================
# MAIN
# =====================================
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
