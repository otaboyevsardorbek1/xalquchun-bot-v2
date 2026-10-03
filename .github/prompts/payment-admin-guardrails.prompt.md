# Payment and admin guardrails

## Role
You are reviewing or editing a production Telegram commerce platform. This prompt applies to payment flows, payout logic, refunds, wallet/balance updates, order approvals, admin moderation, and any operation that changes money or platform trust.

## Non-negotiable rules
- Never invent a successful payment state.
- Orders, transactions, payouts, and refunds must be tied to the real authenticated user and approved business context.
- No guest checkout, no bypass of KYC, no shortcut around blocked-user checks, and no bypass of role authorization.
- Balance, bonus, commission, payout, and refund logic must be traceable and auditable.
- Admin actions must remain logged and must not bypass validation, KYC, or order integrity checks.
- Never expose raw personal data in logs, public responses, or admin output.
- Treat payment and delivery integrations as real provider flows, not placeholders.

## Business and data expectations
- Transaction records must include user linkage, amount, type, status, and admin/audit context when applicable.
- Order totals must come from valid business data, not guessed or stale values.
- Payouts and refunds must preserve a clear approval trail and user consistency.
- Marketplace roles must remain distinct: customer, courier, vendor, dealer, developer, support, admin, super admin.

## Files to inspect first
- [main.py](../../main.py)
- [bot/db/models.py](../../bot/db/models.py)
- [bot/handlers/checkout.py](../../bot/handlers/checkout.py)
- [bot/handlers/admin.py](../../bot/handlers/admin.py)
- [bot/handlers/payment_handlers.py](../../bot/handlers/payment_handlers.py)
- [bot/payment](../../bot/payment)
- [tests/test_checkout_guardrails.py](../../tests/test_checkout_guardrails.py)

## Editing guidance
1. Read the relevant handler, model, and payment service before changing behavior.
2. Preserve the checkout and verification gates before allowing any order or payment flow.
3. Prefer explicit validation and audit logging over shortcut code.
4. Keep admin actions reviewable and traceable.
5. Validate the smallest impacted workflow after the change.

## Failure conditions
Reject any change that:
- allows fake payment completion
- silently credits balance without clear business rules
- bypasses KYC, order validation, or admin approval
- weakens user identity enforcement
- removes auditability for financial or admin actions
