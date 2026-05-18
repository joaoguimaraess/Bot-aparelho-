# 🤖 Bot Telegram — Lembrete dia sim dia não

## Passo 1 — Criar o bot no Telegram

1. Abra o Telegram e procure por **@BotFather**
1. Envie `/newbot`
1. Escolha um nome (ex: `Meu Lembrete`) e um username (ex: `meu_lembrete_bot`)
1. O BotFather vai te dar um **token** — guarde ele (parece: `123456:ABCdef...`)

-----

## Passo 2 — Descobrir seu Chat ID

1. Procure por **@userinfobot** no Telegram
1. Envie qualquer mensagem pra ele
1. Ele responde com seu **Id** — esse é o seu `CHAT_ID`

-----

## Passo 3 — Deploy no Railway

1. Acesse [railway.app](https://railway.app) e crie uma conta (gratuita)
1. Clique em **New Project → Deploy from GitHub repo**
- Ou use **Deploy from local** se preferir fazer upload direto
1. Suba os arquivos: `bot.py` e `requirements.txt`
1. Vá em **Variables** e adicione as duas variáveis de ambiente:
   
   |Nome       |Valor                      |
   |-----------|---------------------------|
   |`BOT_TOKEN`|o token que o BotFather deu|
   |`CHAT_ID`  |seu ID numérico do Telegram|
1. Em **Settings → Start Command**, coloque:
   
   ```
   python bot.py
   ```
1. Clique em **Deploy** ✅

-----

## Como funciona

- O bot roda 24/7 na nuvem
- Todo dia às **22:30 (horário de Brasília)** ele verifica se é dia de enviar
- O primeiro envio é **19/05/2026**, depois dia sim dia não
- A mensagem que aparece no Telegram é: *“🦷 Lembrete: coloque o aparelho hoje à noite!”*

-----

## Quer mudar a mensagem?

Edite a linha no `bot.py`:

```python
text="🦷 Lembrete: coloque o aparelho hoje à noite!"
```

## Quer mudar o horário?

Edite:

```python
scheduler.add_job(enviar_aviso, "cron", hour=22, minute=30)
```