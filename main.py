import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Ambil token & webhook URL dari environment
TOKEN = os.environ.get("BOT_TOKEN") or "ISI_TOKEN_DISINI"
WEBHOOK_URL = os.environ.get("WEBHOOK_URL") or "https://dino-miner-bot.onrender.com"

# Fungsi /start — tampilan awal game
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name or user.username or "Penambang"

    keyboard = [
        [InlineKeyboardButton("🪓 Mulai Menambang", callback_data="mine")],
        [InlineKeyboardButton("📊 Profil", callback_data="profile"),
         InlineKeyboardButton("🏪 Toko", callback_data="shop")],
        [InlineKeyboardButton("🎁 Airdrop", callback_data="airdrop")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f"""🌋 Selamat Datang di 🌋  
🐾 *Jurassic Mining World* 🐾

👷‍♂️ Penambang: *{name}*
🎮 Level: 1
🪙 DinoCoin: 0
⛏️ Alat: Pickaxe Lv.1
🦖 Karakter: 🦕 Dino Basic

🎯 Tujuanmu: Tambang koin, buka karakter, dan jadi legenda dinosaurus!

───────────────
Pilih aksi di bawah ⬇️"""

    await update.message.reply_markdown(text, reply_markup=reply_markup)

# Fungsi handler tombol (callback)
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    if data == "mine":
        await query.edit_message_text("⛏️ Kamu mulai menambang... Tunggu hasilnya!")
    elif data == "profile":
        await query.edit_message_text("📊 Ini profil kamu...\nLevel 1\n🪙 DinoCoin: 0\n⛏️ Alat: Pickaxe Lv.1\n🦕 Karakter: Dino Basic")
    elif data == "shop":
        await query.edit_message_text("🏪 Selamat datang di Toko Dino!\nBelum ada item tersedia.")
    elif data == "airdrop":
        await query.edit_message_text("🎁 Kamu klaim 20 DinoCoin dari airdrop!")

# Jalankan bot dengan webhook
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))

    # Webhook endpoint
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=f"{WEBHOOK_URL}/webhook"
    )
