import asyncio
import os
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Inisialisasi client Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

system_instruction = (
    "Nama kamu adalah Vinaa AI. Kamu adalah asisten pribadi yang ramah, pintar, "
    "dan seru diajak ngobrol. Gunakan bahasa Indonesia yang santai dan akrab."
)

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    user_text = update.message.text
    try:
        # Panggil API Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text,
            config={"system_instruction": system_instruction}
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("Duh, maaf ya Vinaa lagi ada kendala koneksi nih.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    print("Vinaa AI siap melayani...")
    app.run_polling()
