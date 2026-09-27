# XalqUchun Bot

This project is a Telegram bot application with catalog, cart, checkout, referral, and admin workflows.

## Local development

1. Copy `.env.example` to `.env`
2. Fill in the required values
3. Install dependencies:

```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Docker

```bash
docker compose up --build
```

## Health checks

The app exposes:

- `http://localhost:8081/healthz`
- `http://localhost:8081/readyz`

## Production deployment

Set these variables in `.env`:

```env
BOT_TOKEN=your_bot_token
OWNER_ID=your_telegram_user_id
ADMIN_IDS=123456789
WEBHOOK_HOST=https://your-domain.example
WEBHOOK_PATH=/webhook
WEB_SERVER_HOST=0.0.0.0
WEB_SERVER_PORT=8080
HEALTHCHECK_ENABLED=true
HEALTHCHECK_PORT=8081
```

Then run the app normally; it will use webhook mode whenever `WEBHOOK_HOST` is configured.

### Docker production

```bash
docker compose -f docker-compose.prod.yml up --build -d
```

### Health check

```bash
curl http://localhost:8081/healthz
```

### Reverse proxy suggestion

If you are deploying behind Nginx or Caddy, expose the bot only on the webhook port and keep the health endpoint on 8081 or behind the same proxy. Make sure the external endpoint resolves to:

```text
https://your-domain.example/webhook
```
