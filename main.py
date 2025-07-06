from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
import os
import time

DATA_FILE = "userdata.json"

# Inisialisasi file data kalau belum ada
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# Command /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()

    if user_id not in data:
        data[user_id] = {
            "balance": 0,
            "last_mine": 0,
            "level": 1
        }
        save_data(data)

    await update.message.reply_text("Welcome to Dino Miner Bot!")

# Command /mine
async def mine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_data()

    if user_id not in data:
        await update.message.reply_text("Ketik /start dulu ya!")
        return

    now = int(time.time())
    last_mine = data[user_id]["last_mine"]
    cooldown = 8 * 60 * 60  # 8 jam
    time_left = last_mine + cooldown - now

    if time_left > 0:
        hours = time_left // 3600
        minutes = (time_left % 3600) // 60
        await update.message.reply_text(f"⛏️ Kamu harus menunggu {hours} jam {minutes} menit lagi untuk mining lagi.")
        return

    # Hitung reward berdasarkan level
    level = data[user_id].get("level", 1)
    reward = 10 + (level - 1) * 2

    data[user_id]["balance"] += reward
    data[user_id]["last_mine"] = now
    save_data(data)

    await update.message.reply_text(f"🪙 Kamu menambang {reward} DinoCoin!\n💰 Total: {data[user_id]['balance']} DinoCoin")

# Bot Setup
TOKEN = os.environ.get("BOT_TOKEN") or "ISI_TOKEN_BOT_LO_DISINI"
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("mine", mine))

# Jalankan polling
if __name__ == "__main__":
    app.run_polling()
