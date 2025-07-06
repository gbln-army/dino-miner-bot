from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Dino Miner Bot!")

if __name__ == "__main__":
    import os

    TOKEN = os.environ.get("BOT_TOKEN") or "ISI_TOKEN_BOT_LO_DISINI"

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    app.run_polling()
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return "Dino Miner Bot Aktif!"

def run():
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run).start()
