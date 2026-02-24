import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from core.worker import add_to_queue, queue_worker, get_queue_status

# ==============================
# Comandos do bot
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Olá! Eu sou seu bot de streaming de animes.\n\n"
        "Use /download <link> para baixar um vídeo.\n"
        "Use /fila para ver a fila atual."
    )

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "❌ Você precisa enviar o link. Ex:\n/download <link>"
        )
        return

    url = context.args[0]
    msg = await update.message.reply_text("⏳ Preparando download...")
    add_to_queue(update.effective_chat.id, url, msg)

async def fila(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = get_queue_status()
    await update.message.reply_text(status)

# ==============================
# Inicialização do bot
# ==============================
def main():
    TOKEN = "SEU_TOKEN_AQUI"  # substitua pelo token do Telegram
    app = ApplicationBuilder().token(TOKEN).build()

    # Adiciona handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("download", download))
    app.add_handler(CommandHandler("fila", fila))

    # Inicia worker em background
    asyncio.create_task(queue_worker(app))

    # Inicia polling (não usar asyncio.run)
    print("Bot iniciado...")
    app.run_polling()

# ==============================
# Entrypoint
# ==============================
if __name__ == "__main__":
    main()
