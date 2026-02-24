import asyncio
from collections import deque
from streaming.stream_http import stream_to_telegram
from streaming.link_resolver import resolve_link

# ----------------------------
# FILA DE DOWNLOAD
# ----------------------------
DOWNLOAD_QUEUE = deque()
IS_DOWNLOADING = False

# ----------------------------
# Função de progresso para Telegram
# ----------------------------
async def progress_callback(filename, downloaded, total_size, percent, bar):
    """
    Função que envia a barra de progresso pro Telegram
    """
    from telegram import Update  # import local pra evitar loop de import
    if total_size:
        text = (
            f"📥 Baixando vídeo\n\n"
            f"🎬 Nome: {filename}\n"
            f"📦 Tamanho: {downloaded/(1024*1024):.2f}MB / {total_size/(1024*1024):.2f}MB\n\n"
            f"{bar} {percent:.1f}%"
        )
    else:
        text = (
            f"📥 Baixando vídeo\n\n"
            f"🎬 Nome: {filename}\n"
            f"📦 Tamanho: Desconhecido\n\n"
            f"{bar} {percent:.1f}%"
        )

    try:
        # atualiza mensagem original
        await UPDATE_MESSAGE.edit_text(text)
    except Exception:
        pass

# ----------------------------
# Worker principal
# ----------------------------
async def queue_worker(app):
    global IS_DOWNLOADING

    while True:
        if DOWNLOAD_QUEUE and not IS_DOWNLOADING:
            task = DOWNLOAD_QUEUE.popleft()
            chat_id = task["chat_id"]
            url = task["url"]
            global UPDATE_MESSAGE
            UPDATE_MESSAGE = task["msg"]

            IS_DOWNLOADING = True
            try:
                # resolve link (Drive/CDN)
                final_url = await resolve_link(url)
                # faz streaming direto pro Telegram
                await stream_to_telegram(app, chat_id, final_url, progress_callback)
            except Exception as e:
                await app.bot.send_message(chat_id, f"❌ Erro ao baixar vídeo:\n{e}")
            finally:
                IS_DOWNLOADING = False
        await asyncio.sleep(1)

# ----------------------------
# Adiciona tarefa à fila
# ----------------------------
def add_to_queue(chat_id, url, msg):
    """
    Adiciona download à fila
    """
    DOWNLOAD_QUEUE.append({
        "chat_id": chat_id,
        "url": url,
        "msg": msg
    })

# ----------------------------
# Visualizar fila
# ----------------------------
def get_queue_status():
    if not DOWNLOAD_QUEUE:
        return "✅ Fila vazia"
    return f"📌 {len(DOWNLOAD_QUEUE)} vídeo(s) na fila"
