from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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
