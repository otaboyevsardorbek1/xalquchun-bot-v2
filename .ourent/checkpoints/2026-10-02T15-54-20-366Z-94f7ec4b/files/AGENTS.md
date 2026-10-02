# AGENTS.md

## Project overview
This repository is a production-oriented Telegram commerce platform built around a multi-vendor marketplace and delivery ecosystem. The business model follows the XalqUchun architecture described in [tz_contend.md](tz_contend.md): Developer Partner → Dealer → Vendor → Customer and Courier.

Key entry points and conventions:
- Runtime entry: [main.py](main.py)
- Configuration and environment validation: [bot/config.py](bot/config.py)
- Database models and business entities: [bot/db/models.py](bot/db/models.py)
- Bot handlers and workflows: [bot/handlers](bot/handlers)
- Payments and provider integrations: [bot/payment](bot/payment)
- Shared security and auth rules: [bot/middlewares](bot/middlewares)
- Local docs: [README.md](README.md)

## Business architecture from TZ
The platform is not a toy bot. It behaves like a full digital commerce ecosystem with these roles:

- Customer: browses products, places orders, tracks delivery, uses wallet/referral flow.
- Courier: receives assignments, follows delivery route, confirms delivery, earns payout.
- Vendor: manages products, stock, orders, pricing, and payouts.
- Dealer: manages vendor network, supplies products, monitors commissions and distribution.
- Developer Partner: creates/owns products, manages brand and royalty agreements.
- Admin: moderates stores, users, orders, invoices, payouts, KYC and audit logs.
- Super Admin: owns platform-level settings, legal/financial controls and escalation.
- Support: handles user requests, order issues, and customer service operations.

The platform is organized around a clear chain:

Developer Partner -> Dealer -> Vendor -> Customer -> Courier

This means every feature must preserve user identity, role boundaries, financial correctness, and ordering auditability.

## Required working rules for AI agents
Treat every change as production-facing commerce logic. Do not lower business or safety requirements.

1. No guest checkout is allowed.
2. Registration is required before purchase.
3. Required user data includes full name, phone number, delivery address, and ID/passport data.
4. Only verified users may access the purchase flow and place live orders.
5. Unregistered or unverified users must be redirected to complete registration before checkout.
6. Users who pass verification may place orders; unverified users remain blocked until required profile data is collected and approved.
7. Never bypass auth, maintenance mode, blocked-user checks, or role validation.
8. Never expose raw PII in logs, admin messages, debug output, or public responses.
9. Cart, checkout, payment, and order states must remain linked to the authenticated user.
10. Real payment and delivery logic must use provider-style adapters, not fake success states.
11. Admin actions must remain auditable and must not bypass KYC, order validation, or financial controls.
12. Financial flows must remain consistent: balance, commission, payout, bonus, and refund logic must not allow unauthorized credits.
13. Multi-role operations must respect panel boundaries: customer, vendor, dealer, developer, courier, and admin responsibilities are distinct.
14. Real-time order and fulfillment state changes must remain traceable and auditable.

## Platform expectations from the TZ model
- Web coding pattern: browser-based panels, Telegram navigation, and a unified backend.
- FastAPI + React + Telegram Bot + WebSocket stack is the intended architecture for live operations.
- Redis, PostgreSQL, and async workers should be treated as core platform components, not optional extras.
- Every order must carry delivery metadata, contact number, status history, and user identity.
- The system must support transaction types such as payment, payout, bonus, refund, and manual processing.
- KYC, address validation, phone validation, and audit logs are not optional features; they are business-critical controls.

## Security and data protection
- Validate every incoming phone number, address, and identity field.
- Minimize logging of sensitive data and redact personal information in errors and internal logs.
- Reject incomplete or inconsistent personal data before a user enters live order flow.
- Keep sensitive data in secure storage and follow least-privilege access for admin and support roles.
- Prefer environment-driven configuration over hard-coded secrets or IDs.

## Production-readiness expectations
- Keep config values in environment variables, not inside code.
- Respect webhook, health check, and maintenance deployment conventions.
- Preserve role checks and status gates for blocked or suspended users.
- Keep business rules explicit; do not create guest or shortcut checkout paths.
- Protect the separation of bot UI, business rules, and persistence logic.

## High-value files to inspect first
1. [main.py](main.py) — router bootstrap and runtime wiring
2. [bot/config.py](bot/config.py) — environment and security configuration
3. [bot/db/models.py](bot/db/models.py) — user, order, and financial data models
4. [bot/handlers/checkout.py](bot/handlers/checkout.py) — order flow and gating
5. [bot/handlers/profile.py](bot/handlers/profile.py) — user verification and KYC workflow
6. [bot/handlers/admin.py](bot/handlers/admin.py) — admin controls and audit actions
7. [README.md](README.md) — deployment and platform notes
8. [tz_contend.md](tz_contend.md) — full ecosystem specification and business model

## Recommended implementation direction
When adding features, prefer a clean architecture:
- bot handlers handle user interaction only
- business services manage validation and commerce logic
- database models represent real entities and relationships
- payment and delivery services use provider-style adapters
- admin workflows must use audit logs and approval steps

This keeps the system aligned with the real-world business model described in the TZ document and avoids shortcuts that weaken trust or financial safety.
