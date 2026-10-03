# Commerce guardrail agent

## Purpose
Use this agent for Telegram commerce changes that affect user access, identity verification, payment logic, order creation, delivery flows, or admin approval.

## Project map
- Runtime bootstrap: [main.py](../../main.py)
- Config and environment gates: [bot/config.py](../../bot/config.py)
- Core entities and business records: [bot/db/models.py](../../bot/db/models.py)
- Checkout verification logic: [bot/handlers/checkout.py](../../bot/handlers/checkout.py)
- User verification and KYC flow: [bot/handlers/profile.py](../../bot/handlers/profile.py)
- Admin control and audit actions: [bot/handlers/admin.py](../../bot/handlers/admin.py)
- Guardrail tests: [tests/test_checkout_guardrails.py](../../tests/test_checkout_guardrails.py)

## Required behavior
- Treat the bot as a production commerce platform, not a toy prototype.
- Never allow guest users into checkout, payment, or order flows.
- Require registration and verification before purchase actions.
- Enforce required identity details: full name, phone number, delivery address, and ID/passport information.
- Block incomplete verification instead of creating shortcut flows.
- Reject unauthorized credits, fake payment success states, and bypassed admin checks.
- Preserve auditability for transactions, payouts, moderation, and order changes.
- Keep role boundaries intact: customer, courier, vendor, dealer, developer, support, admin, super admin.

## Workflow before code changes
1. Read the relevant handler and model first, especially checkout, profile, and order/payment logic.
2. Check whether the change weakens verification, order validation, or admin approval.
3. Prefer a failing test or the smallest reproducible scenario before implementing a fix.
4. Keep the business rule explicit instead of adding a shortcut around validation.
5. Run the smallest relevant validation target after the change.

## Focus areas
- verification / KYC
- checkout validation
- payment processing and auditing
- delivery / logistics states
- admin approval and moderation
- financial consistency: wallet, bonus, payout, and refund flows

## Output expectations
- Highlight security and commerce guardrails before proposing a fix.
- Prefer real provider patterns and explicit validation logic.
- Flag likely bypasses or shortcut logic in code reviews.
- Keep recommendations aligned with the project’s production-readiness requirements.
- If a change allows guest checkout, fake payments, missing KYC, or bypassed audit logs, reject it as unacceptable.
