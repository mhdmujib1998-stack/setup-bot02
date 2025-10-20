import os
import hashlib
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ===== CONFIG =====
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise SystemExit("❌ BOT_TOKEN belum diset. Tambahkan environment variable BOT_TOKEN terlebih dahulu.")

# Template sambutan (gunakan {name}, {id}, {code})
WELCOME_TEMPLATE = os.getenv(
    "WELCOME_MESSAGE",
    (
        "🎉 Selamat datang boskuu di AGENJITU303, {name}! 🎮\n\n"
        "🔥 Kami senang banget kamu bergabung bersama kami!\n"
        "Berikut identitasmu di AGENJITU303 ini:\n"
        "🆔 ID: {id}\n"
        "🎯 Kode Member: {code}\n\n"
        "⚡ Nikmati keseruan, ikuti event, dan jadilah bagian dari tim pemenang! 💪"
    )
)

# ===== UTILITIES =====
def make_user_code(user_id: int) -> str:
    """Buat kode unik 6 huruf/angka dari user_id."""
    h = hashlib.sha1(str(user_id).encode("utf-8")).hexdigest()
    return h[:6].upper()

# ===== HANDLERS =====
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Halo! Saya siap menyapa anggota baru dengan gaya keren dan penuh semangat!"
    )

async def greet_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.new_chat_members:
        return

    for u in msg.new_chat_members:
        try:
            name = u.first_name or u.username or "Pengguna"
            uid = getattr(u, "id", None)
            code = make_user_code(uid) if uid else "N/A"

            text = WELCOME_TEMPLATE.format(name=name, id=uid, code=code)
            await msg.reply_text(text)
            print(f"✅ Menyambut {name} (ID: {uid}, Code: {code})")
        except Exception as e:
            print(f"⚠️ Gagal menyapa anggota baru: {e}")

# ===== MAIN =====
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_new_members))

    print("🤖 Bot aktif — siap menyapa anggota baru dengan ID dan kode unik!")
    app.run_polling()

if __name__ == "__main__":
    main()
