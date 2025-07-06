from flask import Flask
import threading
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

app = Flask(__name__)

@app.route('/')
def index():
    return "Dino Miner Bot Aktif!"

# Fungsi bot Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Dino Miner Bot!")

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def run_bot():
    TOKEN = os.environ.get("BOT_TOKEN") or "ISI_TOKEN_BOT_LO_DISINI"
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    # Jalanin Flask di thread terpisah
    threading.Thread(target=run_flask).start()
    
    # Jalanin bot utama
    run_bot()
