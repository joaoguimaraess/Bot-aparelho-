import os
import asyncio
from datetime import datetime, date
import pytz
from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ─── CONFIGURAÇÃO ────────────────────────────────────────────────
BOT_TOKEN  = os.environ["BOT_TOKEN"]   # Token do BotFather
CHAT_ID    = os.environ["CHAT_ID"]     # Seu chat ID (veja README)
TIMEZONE   = "America/Sao_Paulo"

# Data de início (primeiro dia que deve enviar a mensagem)
# Formato: YYYY, MM, DD
START_DATE = date(2026, 5, 19)
# ─────────────────────────────────────────────────────────────────

async def deve_enviar_hoje() -> bool:
    hoje = datetime.now(pytz.timezone(TIMEZONE)).date()
    delta = (hoje - START_DATE).days
    return delta >= 0 and delta % 2 == 0

async def enviar_aviso():
    if not await deve_enviar_hoje():
        print("Hoje não é dia de enviar.")
        return

    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(
        chat_id=CHAT_ID,
        text="🦷 Lembrete: coloque o aparelho hoje à noite!"
    )
    print(f"Mensagem enviada em {datetime.now()}")

async def main():
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    scheduler.add_job(enviar_aviso, "cron", hour=22, minute=30)
    scheduler.start()
    print("Bot rodando... aguardando 22:30 🤖")
    await asyncio.Event().wait()  # roda pra sempre

if __name__ == "__main__":
    asyncio.run(main())
