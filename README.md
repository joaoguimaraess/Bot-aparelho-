# 🦷 Bot Telegram — Lembrete do Aparelho

Bot que avisa dia sim dia não às 22:30 para colocar o aparelho, com confirmação, streak e comandos.

-----

## Passo 1 — Criar o bot no Telegram

1. Abra o Telegram e procure por **@BotFather**
1. Envie `/newbot`
1. Escolha um nome (ex: `Meu Lembrete`) e um username (ex: `meu_lembrete_bot`)
1. O BotFather vai te dar um **token** — guarde ele (parece: `123456:ABCdef...`)
1. Abra o seu bot e clique em **Start** para ativá-lo

-----

## Passo 2 — Descobrir seu Chat ID

1. Acesse no navegador (substituindo pelo seu token):
   
   ```
   https://api.telegram.org/bot<SEU_TOKEN>/getUpdates
   ```
1. Procure por `"chat": { "id": 123456789` — esse número é o seu `CHAT_ID`
- Se o resultado vier vazio, mande uma mensagem pro bot primeiro e tente de novo

-----

## Passo 3 — Deploy no Railway

1. Acesse [railway.app](https://railway.app) e crie uma conta (gratuita)
1. Suba os arquivos `bot.py` e `requirements.txt` no GitHub
1. No Railway: **New Project → Deploy from GitHub repo**
1. Vá em **Variables** e adicione:
   
   |Nome       |Valor                      |
   |-----------|---------------------------|
   |`BOT_TOKEN`|o token que o BotFather deu|
   |`CHAT_ID`  |seu ID numérico (sem aspas)|
1. Em **Settings → Start Command**, coloque:
   
   ```
   python bot.py
   ```
1. Clique em **Deploy** ✅

-----

## Como usar

### Lembrete automático

Todo dia às **22:30 (horário de Brasília)** o bot verifica se é dia de enviar e manda uma mensagem aleatória. O primeiro envio é **20/05/2026**, depois dia sim dia não.

Se você não confirmar em **30 minutos**, o bot manda um lembrete de reforço 😅

### Confirmar que colocou

Responda ao bot com o emoji **✅** — ele confirma e atualiza seu streak.

### Comandos disponíveis

|Comando  |O que faz                             |
|---------|--------------------------------------|
|✅        |Confirma que colocou o aparelho       |
|`/status`|Mostra situação do dia, streak e total|
|`/pular` |Pula o dia de hoje sem perder o streak|
|`/ajuda` |Lista todos os comandos               |

### Streak 🔥

O bot celebra nas marcas de **3, 7, 14 e 30 dias** seguidos sem esquecer!

-----

## Personalizações

### Mudar o horário

```python
scheduler.add_job(..., hour=22, minute=30)
```

### Mudar ou adicionar mensagens

Edite a lista `MENSAGENS` no início do `bot.py`.

### Mudar a data de início

```python
START_DATE = date(2026, 5, 20)
```