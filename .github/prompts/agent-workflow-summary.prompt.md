# Agent workflow summary prompt

## Role
You are working inside the XalqUchun commerce platform. This prompt is for quick onboarding, consistent implementation, and safe agent execution across the project.

## Default operating path
Use this sequence for most changes:
1. Read the relevant handler and model first.
2. Confirm the business rule and role boundary affected.
3. Check whether the change touches checkout, KYC, payment, payout, delivery, admin, or marketplace logic.
4. Prefer a failing test or smallest reproduction before editing.
5. Implement the minimal root-cause fix.
6. Validate the smallest relevant workflow.

## Required repo context
Always keep these facts in mind:
- The project is a real marketplace and delivery ecosystem, not a toy bot.
- The role chain is Developer Partner → Dealer → Vendor → Customer → Courier.
- Guest checkout is forbidden.
- Registration and verification are required before real order flow.
- Full name, phone, address, and identity data must be validated.
- Real payment and delivery flows must not be replaced with fake success states.
- Admin and financial actions must remain auditable.

## Key files
- [main.py](../../main.py)
- [bot/config.py](../../bot/config.py)
- [bot/db/models.py](../../bot/db/models.py)
- [bot/handlers/checkout.py](../../bot/handlers/checkout.py)
- [bot/handlers/profile.py](../../bot/handlers/profile.py)
- [bot/handlers/admin.py](../../bot/handlers/admin.py)
- [bot/services/marketplace.py](../../bot/services/marketplace.py)
- [bot/services/order_service.py](../../bot/services/order_service.py)
- [tz_contend.md](../../tz_contend.md)
- [tests/test_checkout_guardrails.py](../../tests/test_checkout_guardrails.py)

## Hard stop rules
Reject or flag any change that:
- bypasses verification or guest-blocking rules
- allows fake payment or fake delivery completion
- removes role boundaries or audit logs
- silently credits wallets or changes payouts without business reason
- weakens customer identity, KYC, or order validation

## Output standard
When proposing or implementing a fix, state:
- what business rule is affected
- which role or flow is impacted
- what validation or test was checked
- whether the change preserves auditability and safety
