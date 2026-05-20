import os
import asyncio
import json
import random
from datetime import datetime, date, timedelta
from pathlib import Path
import pytz
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ─── CONFIGURAÇÃO ────────────────────────────────────────────────
BOT_TOKEN  = os.environ["BOT_TOKEN"]
CHAT_ID    = int(os.environ["CHAT_ID"])
TIMEZONE   = "America/Sao_Paulo"
START_DATE = date(2026, 5, 19)
DATA_FILE  = "dados.json"
# ─────────────────────────────────────────────────────────────────

MENSAGENS = [
    "🦷 Hora de colocar o aparelho! Bora lá 💪",
    "🦷 Não esquece do aparelho hoje à noite!",
    "🦷 Aparelho na boca = sorriso no futuro 😁",
    "🦷 Seu eu do futuro agradece — coloca o aparelho!",
    "🦷 Chegou a hora! Aparelho, vai lá.",
    "🦷 Lembretinho carinhoso: aparelho, por favor 🙏",
    "🦷 Mais um dia, mais um passo pro sorriso perfeito!",
]

# ─── PERSISTÊNCIA ────────────────────────────────────────────────

def carregar_dados() -> dict:
    if Path(DATA_FILE).exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"confirmados": [], "pulados": [], "streak": 0, "ultimo_confirmado": None}

def salvar_dados(dados: dict):
    with open(DATA_FILE, "w") as f:
        json.dump(dados, f)

# ─── LÓGICA DO DIA ───────────────────────────────────────────────

def hoje_str() -> str:
    return datetime.now(pytz.timezone(TIMEZONE)).strftime("%Y-%m-%d")

def deve_enviar_hoje() -> bool:
    hoje = datetime.now(pytz.timezone(TIMEZONE)).date()
    delta = (hoje - START_DATE).days
    return delta >= 0 and delta % 2 == 0

def calcular_streak(dados: dict) -> int:
    confirmados = set(dados.get("confirmados", []))
    pulados = set(dados.get("pulados", []))
    streak = 0
    hoje = datetime.now(pytz.timezone(TIMEZONE)).date()
    delta_total = (hoje - START_DATE).days

    for i in range(delta_total, -1, -2):
        d = START_DATE + timedelta(days=i)
        ds = d.strftime("%Y-%m-%d")
        if ds in confirmados or ds in pulados:
            streak += 1
        else:
            break
    return streak

# ─── ENVIO DO LEMBRETE ───────────────────────────────────────────

async def enviar_aviso(bot: Bot):
    dados = carregar_dados()
    hoje = hoje_str()

    if hoje in dados.get("pulados", []):
        print(f"Dia {hoje} foi pulado, sem envio.")
        return

    if not deve_enviar_hoje():
        print(f"Hoje ({hoje}) não é dia de enviar.")
        return

    msg = random.choice(MENSAGENS)
    await bot.send_message(
        chat_id=CHAT_ID,
        text=msg + "\n\nResponda ✅ para confirmar ou use /pular se não for usar hoje."
    )
    print(f"Lembrete enviado: {hoje}")

    # Lembrete de reforço após 30 min se não confirmado
    await asyncio.sleep(1800)
    dados = carregar_dados()
    if hoje not in dados.get("confirmados", []) and hoje not in dados.get("pulados", []):
        await bot.send_message(
            chat_id=CHAT_ID,
            text="⏰ Ainda não confirmou! Não esquece do aparelho, hein 😅"
        )

# ─── COMANDOS ────────────────────────────────────────────────────

async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dados = carregar_dados()
    hoje = hoje_str()

    eh_dia = deve_enviar_hoje()
    confirmado = hoje in dados.get("confirmados", [])
    pulado = hoje in dados.get("pulados", [])
    streak = calcular_streak(dados)
    total = len(dados.get("confirmados", []))

    if not eh_dia:
        status = "😴 Hoje não é dia de colocar — descanse!"
    elif confirmado:
        status = "✅ Já confirmado hoje!"
    elif pulado:
        status = "⏭️ Pulado hoje."
    else:
        status = "⏳ Aguardando confirmação..."

    texto = (
        f"📊 *Status do aparelho*\n\n"
        f"{status}\n\n"
        f"🔥 Streak atual: *{streak} dias*\n"
        f"✅ Total confirmados: *{total} dias*"
    )
    await update.message.reply_text(texto, parse_mode="Markdown")

async def cmd_pular(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dados = carregar_dados()
    hoje = hoje_str()
    if hoje not in dados["pulados"]:
        dados["pulados"].append(hoje)
        salvar_dados(dados)
    await update.message.reply_text("⏭️ Ok! Dia de hoje pulado. Sem cobranças 😌")

async def cmd_ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🦷 *Bot do Aparelho*\n\n"
        "Comandos disponíveis:\n"
        "✅ — Confirmar que colocou o aparelho\n"
        "/status — Ver streak e situação do dia\n"
        "/pular — Pular o dia de hoje\n"
        "/ajuda — Ver esta mensagem",
        parse_mode="Markdown"
    )

async def handle_confirmacao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    if "✅" not in texto:
        return

    dados = carregar_dados()
    hoje = hoje_str()

    if hoje in dados.get("confirmados", []):
        await update.message.reply_text("Já tinha confirmado hoje! 😄")
        return

    dados["confirmados"].append(hoje)
    streak = calcular_streak(dados)
    dados["streak"] = streak
    dados["ultimo_confirmado"] = hoje
    salvar_dados(dados)

    if streak >= 30:
        extra = f"\n\n🏆 INCRÍVEL! {streak} dias seguidos! Você é imparável!"
    elif streak >= 14:
        extra = f"\n\n🔥 {streak} dias seguidos! Que consistência!"
    elif streak >= 7:
        extra = f"\n\n⚡ {streak} dias seguidos! Tá pegando fogo!"
    elif streak >= 3:
        extra = f"\n\n💪 {streak} dias seguidos! Continua assim!"
    else:
        extra = f"\n\n🔥 Streak: {streak} dia(s)!"

    await update.message.reply_text(f"✅ Confirmado! Bora sorrir lindo 😁{extra}")

# ─── MAIN ────────────────────────────────────────────────────────

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    bot = app.bot

    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("pular", cmd_pular))
    app.add_handler(CommandHandler("ajuda", cmd_ajuda))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_confirmacao))

    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    scheduler.add_job(enviar_aviso, "cron", hour=22, minute=30, args=[bot])
    scheduler.start()

    print("🤖 Bot rodando! Aguardando 22:30...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
