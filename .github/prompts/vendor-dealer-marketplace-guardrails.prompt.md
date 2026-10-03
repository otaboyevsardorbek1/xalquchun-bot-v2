# Vendor and dealer marketplace guardrails

## Role
You are reviewing or editing the marketplace layer of a production Telegram commerce ecosystem. This prompt applies to dealer operations, vendor catalog management, product listing, commissions, stock handling, payouts, and partner-level access control.

## Non-negotiable rules
- Marketplace roles must remain distinct and non-overlapping: Developer Partner, Dealer, Vendor, Customer, Courier, Support, Admin, Super Admin.
- A dealer or vendor must never bypass customer verification, order validation, KYC gates, or admin approvals.
- Product, pricing, stock, and payout actions must remain tied to the authenticated business actor and real business context.
- No fake sales confirmations, fake payout approvals, or placeholder marketplace operations.
- Customer identity and delivery data must remain protected and not exposed in logs or public output.
- Real provider-style integrations should be used for money movement, stock updates, and partner operations.

## Business and data expectations
- Orders and payouts must retain audit evidence and user linkage.
- Dealer/vendor actions should be scoped to their business boundaries and not permit cross-role privilege escalation.
- Commission, royalty, and payout logic must be consistent and traceable.
- Product or catalog changes must not bypass validation, availability rules, or review requirements.

## Files to inspect first
- [main.py](../../main.py)
- [bot/db/models.py](../../bot/db/models.py)
- [bot/handlers/admin.py](../../bot/handlers/admin.py)
- [bot/handlers/checkout.py](../../bot/handlers/checkout.py)
- [bot/services/marketplace.py](../../bot/services/marketplace.py)
- [bot/services/order_service.py](../../bot/services/order_service.py)
- [tests/test_checkout_guardrails.py](../../tests/test_checkout_guardrails.py)

## Editing guidance
1. Read the relevant marketplace, role, order, and admin logic before changing behavior.
2. Keep role boundaries explicit and enforce them in validation checks.
3. Preserve customer verification, checkout gating, and auditability for all financial actions.
4. Prefer clear services and policy objects over loose permission shortcuts.
5. Validate the smallest impacted marketplace workflow after the change.

## Failure conditions
Reject any change that:
- permits cross-role privilege escalation or silent bypass of role checks
- allows fake payout, fake commission, or fake stock completion
- weakens identity verification for customer or partner actions
- removes traceability for payouts, orders, or product updates
- collapses the real XalqUchun marketplace chain into a generic bot flow
