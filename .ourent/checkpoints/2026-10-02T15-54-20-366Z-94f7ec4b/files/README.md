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

## AI agent guardrails and project rules

This repository keeps a lean, production-oriented guardrail set for future coding agents:

- [AGENTS.md](AGENTS.md) — core repo guidance, role model, and business rules.
- [.github/copilot-instructions.md](.github/copilot-instructions.md) — default rules for all AI-assisted work.
- [.github/instructions/commerce-ecosystem.md](.github/instructions/commerce-ecosystem.md) — consolidated architecture and marketplace rules from the TZ document.
- [.github/prompts/commerce-guardrails.prompt.md](.github/prompts/commerce-guardrails.prompt.md) — reusable commerce-safety review prompt.
- [.github/agents/commerce-guardrail-agent.md](.github/agents/commerce-guardrail-agent.md) — specialized guardrail agent.

All AI-generated or AI-assisted changes must preserve the real-business rules of this system: guest users are blocked from ordering, users must register and complete verification before checkout, required personal data must be validated, and payment and fulfillment flows must follow real provider-style workflows instead of fake shortcuts.

