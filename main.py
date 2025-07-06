from flask import Flask, request import telegram import os import json import time

TOKEN = os.environ.get("BOT_TOKEN", "PUT_YOUR_BOT_TOKEN_HERE") bot = telegram.Bot(token=TOKEN) app = Flask(name)

DATA_FILE = "userdata.json" MINE_COOLDOWN = 8 * 60 * 60 LEVEL_THRESHOLDS = [10, 25, 45, 70, 100, 130, 170, 210, 260, 320]  # Total exp thresholds per level DINO_CHARACTERS = [ ("Baby Raptor", "🐣"), ("Tricera Rookie", "🦕"), ("Speed Raptor", "🦖"), ("Spino Miner", "🐊"), ("Horned Crusher", "🦖💥"), ("T-Rex Tycoon", "👑🦖"), ("Magma Raptor", "🔥🦖"), ("Frozen Spino", "❄️🦕"), ("Cyber Raptor", "🤖🦖"), ("Darkzilla", "🐉🌑"), ("God Dino", "🌟🦕👑") ]

Load user data

def load_data(): if not os.path.exists(DATA_FILE): return {} with open(DATA_FILE, "r") as f: return json.load(f)

Save user data

def save_data(data): with open(DATA_FILE, "w") as f: json.dump(data, f)

Calculate level from exp

def get_level(exp): level = 1 for threshold in LEVEL_THRESHOLDS: if exp >= threshold: level += 1 else: break return min(level, 100)

Get character based on level

def get_character(level): index = min(level // 10, len(DINO_CHARACTERS)-1) return DINO_CHARACTERS[index]

@app.route("/", methods=["POST"]) def webhook(): update = telegram.Update.de_json(request.get_json(force=True), bot) chat_id = str(update.message.chat.id) text = update.message.text

data = load_data()
if chat_id not in data:
    data[chat_id] = {
        "exp": 0,
        "gold": 0,
        "last_mine": 0
    }

user = data[chat_id]
level = get_level(user["exp"])
character_name, character_emoji = get_character(level)

if text == "/start":
    bot.send_message(chat_id, f"Welcome to Dino Miner!\nYou are: {character_name} {character_emoji}\nType /mine to start mining.")

elif text == "/mine":
    now = int(time.time())
    if now - user["last_mine"] >= MINE_COOLDOWN:
        user["last_mine"] = now
        user["gold"] += 10 + level
        user["exp"] += 5
        level = get_level(user["exp"])
        character_name, character_emoji = get_character(level)
        save_data(data)
        bot.send_message(chat_id, f"⛏️ You mined {(10 + level)} GBLN and earned 5 EXP!\nLevel: {level} - {character_name} {character_emoji}")
    else:
        remaining = MINE_COOLDOWN - (now - user["last_mine"])
        h = remaining // 3600
        m = (remaining % 3600) // 60
        bot.send_message(chat_id, f"⏳ You need to wait {h}h {m}m before mining again.")

elif text == "/balance":
    bot.send_message(chat_id, f"💰 Gold: {user['gold']}\n⭐ EXP: {user['exp']}\n🎖️ Level: {level}\n🦕 Character: {character_name} {character_emoji}")

else:
    bot.send_message(chat_id, "Unknown command. Try /mine or /balance")

return "ok"

if name == "main": app.run(debug=True)

