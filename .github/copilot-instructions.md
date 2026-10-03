# Copilot instructions for this commerce bot

## Project context
This repository is a real-world Telegram commerce platform for product sales, checkout, delivery, payments, referral rewards, admin operations, and multi-role marketplace coordination. Treat every feature as production-facing and be aligned with the ecosystem model in [tz_contend.md](../tz_contend.md).

Main files:
- [main.py](../main.py)
- [README.md](../README.md)
- [tz_contend.md](../tz_contend.md)
- [bot/config.py](../bot/config.py)
- [bot/db/models.py](../bot/db/models.py)
- [bot/handlers/checkout.py](../bot/handlers/checkout.py)
- [bot/handlers/profile.py](../bot/handlers/profile.py)
- [bot/handlers/admin.py](../bot/handlers/admin.py)
- [bot/payment](../bot/payment)

## Hard rules
- No guest checkout is allowed.
- Registration is required before purchase.
- Required user data includes full name, phone number, delivery address, and ID/passport data.
- Only verified users may buy products and access the live purchase flow.
- If a user is unverified, the system must request the missing information instead of allowing a shortcut.
- Users must never bypass authentication, maintenance mode, or blocked-user checks.
- Never expose raw personal data in logs, errors, or public messages.
- Real payment and delivery patterns must be used; fake success states are not allowed.
- Treat marketplace, delivery, and fulfillment flows as real business integrations with verification and audit trails.
- Admin actions must remain auditable and must not bypass verification, order validation, or financial safety checks.

## System analysis
This repo is organized around a Telegram commerce workflow with strict gates before a real order can be created. The startup path in [main.py](../main.py) creates the bot, installs middleware (logging, error handling, rate limiting, maintenance, auth), registers the main routers, and initializes the database/cache and health endpoints.

The practical flow is:
1. user starts bot and browses catalog
2. cart is built and validated
3. checkout checks registration, phone number, KYC and blocked state
4. location + delivery details are attached to the order
5. payment resolution uses the real order amount
6. admin operations remain auditable and tied to the underlying user/role

The data model in [bot/db/models.py](../bot/db/models.py) is intentionally business-facing: `User` stores identity and KYC; `Order` and `OrderItem` store delivery/contact/total data; `Transaction` tracks payment/payout/bonus/refund events; `AuditLog` preserves traceable business evidence. Files such as [bot/handlers/checkout.py](../bot/handlers/checkout.py) and [tests/test_checkout_guardrails.py](../tests/test_checkout_guardrails.py) are the best examples of the expected guardrails.

## Commerce ecosystem rules
- The platform follows the XalqUchun chain: Developer Partner → Dealer → Vendor → Customer → Courier.
- Customer, courier, vendor, dealer, developer, admin, super admin, and support roles are distinct and must keep clear boundaries.
- Orders, cart states, transactions, payout requests, and referrals must remain tied to the authenticated user and role.
- Orders must store delivery data, contact number, status history, and audit evidence.
- Transactions may include payment, payout, bonus, refund, or manual processing types, and all must be consistent with business rules.

## Security and data protection
- Validate every incoming phone number, address, and identity field.
- Keep sensitive data in secure storage and minimize logging.
- Reject incomplete or inconsistent personal data before moving the user into a live order flow.
- Follow clear verification for ID/passport confirmation and account approval.
- Prefer explicit role-based checks and approval flows over permissive shortcuts.

## Production expectations
- Prefer environment-driven configuration in [bot/config.py](../bot/config.py) instead of hard-coded secrets or IDs.
- Respect webhook and health-check deployment patterns described in [README.md](../README.md).
- Keep admin, payment, referral, order, and delivery modules separated and clear.
- Prefer explicit business logic over temporary shortcuts that skip validation.
- Use provider-like adapters for payment and delivery integration instead of fake success states.

## Good agent behavior
When modifying this project:
1. Read the relevant handler and business model first.
2. Preserve verification and checkout guardrails.
3. Respect the role hierarchy and marketplace flow described in the TZ document.
4. Prefer real provider adapters for payment and delivery workflows.
5. Validate with the smallest relevant runtime or test check.
6. Keep auditability, KYC, and financial safety intact across each change.

## Minimal rule set to keep forever
If a change weakens customer identity verification, allows guest checkout, creates fake payment completion, skips auditability, or removes role/approval protections, it is not acceptable.
