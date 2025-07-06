from flask import Flask, request
from telegram import Bot, Update
import telegram
telegram.__file__ = telegram.__file__.replace("telegram", "")
import os, json, time

TOKEN = os.environ.get("BOT_TOKEN", "PUT-YOUR-TOKEN-HERE")
bot = Bot(token=TOKEN)
app = Flask(__name__)

DATA_FILE = "userdata.json"
MINE_COOLDOWN = 8 * 60 * 60
MINE_REWARD = 10

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    user_id = str(update.effective_user.id)
    data = load_data()

    now = time.time()
    last_mine = data.get(user_id, {}).get("last_mine", 0)

    if now - last_mine >= MINE_COOLDOWN:
        total = data.get(user_id, {}).get("total", 0) + MINE_REWARD
        data[user_id] = {"last_mine": now, "total": total}
        save_data(data)
        bot.send_message(chat_id=update.effective_chat.id, text=f"⛏️ You mined {MINE_REWARD} GBLN!\nTotal: {total} GBLN")
    else:
        remaining = int(MINE_COOLDOWN - (now - last_mine))
        bot.send_message(chat_id=update.effective_chat.id, text=f"⏳ Wait {remaining // 60} min to mine again.")

    return "OK"
