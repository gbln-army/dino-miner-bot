from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes import os, json, random from datetime import datetime, timedelta

DATA_FILE = "userdata.json"

Fungsi untuk load & simpan data user

def load_data(): if not os.path.exists(DATA_FILE): return {} with open(DATA_FILE, "r") as f: return json.load(f)

def save_data(data): with open(DATA_FILE, "w") as f: json.dump(data, f, indent=2)

Fungsi /start — tampilan awal game

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): user = update.effective_user user_id = str(user.id) name = user.first_name or user.username or "Penambang"

data = load_data()
if user_id not in data:
    data[user_id] = {
        "name": name,
        "coins": 0,
        "level": 1,
        "last_mine": None
    }
    save_data(data)

keyboard = [
    [InlineKeyboardButton("🪓 Mulai Menambang", callback_data="mine")],
    [InlineKeyboardButton("📊 Profil", callback_data="profile"),
     InlineKeyboardButton("🏪 Toko", callback_data="shop")],
    [InlineKeyboardButton("🎁 Airdrop", callback_data="airdrop")]
]

reply_markup = InlineKeyboardMarkup(keyboard)

text = f"""🌋 Selamat Datang di 🌋

🐾 Jurassic Mining World 🐾

👷‍♂️ Penambang: {name} 🎮 Level: 1 🪙 DinoCoin: 0 ⛏️ Alat: Pickaxe Lv.1 🦖 Karakter: 🦕 Dino Basic

🎯 Tujuanmu: Tambang koin, buka karakter, dan jadi legenda dinosaurus!

─────────────── Pilih aksi di bawah ⬇️"""

await update.message.reply_markdown(text, reply_markup=reply_markup)

Fungsi handler tombol (callback)

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query user = query.from_user user_id = str(user.id) data = load_data() await query.answer()

if user_id not in data:
    await query.edit_message_text("Kamu belum mulai game. Gunakan /start dulu!")
    return

if query.data == "mine":
    now = datetime.utcnow()
    last_mine = data[user_id].get("last_mine")
    if last_mine:
        last_time = datetime.fromisoformat(last_mine)
        if now - last_time < timedelta(hours=8):
            remaining = timedelta(hours=8) - (now - last_time)
            mins = int(remaining.total_seconds() // 60)
            await query.edit_message_text(f"⛏️ Kamu sudah menambang! Tunggu {mins} menit lagi untuk menambang lagi.")
            return

    coins_earned = random.randint(5, 15)
    data[user_id]["coins"] += coins_earned
    data[user_id]["last_mine"] = now.isoformat()
    save_data(data)

    await query.edit_message_text(f"⛏️ Kamu menambang {coins_earned} DinoCoin!\n💰 Total: {data[user_id]['coins']} DinoCoin")

elif query.data == "profile":
    user_data = data[user_id]
    await query.edit_message_text(
        f"📊 Profil Penambang:

👷‍♂️ Nama: {user_data['name']} 🎮 Level: {user_data['level']} 🪙 DinoCoin: {user_data['coins']}")

elif query.data == "shop":
    await query.edit_message_text("🏪 Selamat datang di Toko Dino!")

elif query.data == "airdrop":
    data[user_id]['coins'] += 20
    save_data(data)
    await query.edit_message_text("🎁 Kamu klaim 20 DinoCoin dari airdrop!")

Bagian utama aplikasi bot

if name == "main": TOKEN = os.environ.get("BOT_TOKEN") or "ISI_TOKEN_BOT_LO_DISINI" app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_buttons))

app.run_polling()

