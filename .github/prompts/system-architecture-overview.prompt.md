# System architecture overview prompt

## Role
You are working on a production Telegram commerce platform that implements the XalqUchun ecosystem. This prompt is for high-level architecture decisions, component boundaries, and product understanding across the entire business stack.

## Core app model
The system is not a simple bot. It is a marketplace and delivery ecosystem built around this chain:

Developer Partner → Dealer → Vendor → Customer → Courier

The app combines:
- Telegram bot interactions and messaging
- web-based panels for customer, vendor, dealer, developer, courier, admin, and support roles
- an async backend and shared business logic
- database-backed order, finance, KYC, and audit records
- real-time events and notifications
- external provider integrations for payments, SMS, maps, and messaging

## Product and domain areas
- Customer experience: catalog, cart, checkout, order tracking, wallet, referrals, profile, and support
- Vendor operations: product catalog, inventory, order acceptance, payouts, and analytics
- Dealer operations: network management, distribution, commissions, and onboarding
- Developer Partner operations: product ownership, royalties, distribution agreements, and brand management
- Courier flow: assignment, route management, tracking, delivery confirmation, and earnings
- Admin and support: moderation, verification, approvals, audits, financial safety, and dispute handling

## Architectural expectations
- Keep business logic separated from handler/UI logic.
- Treat role boundaries as explicit contracts, not generic user states.
- Keep verification, order validation, payment flow, and delivery flow tied to the authenticated user and business rules.
- Prefer provider-style adapters for payment, SMS, maps, and fulfillment integration.
- Use audit logs for critical financial and operational actions.
- Maintain a clear distinction between bot interface logic, web panel logic, and backend business services.

## Files to inspect first
- [main.py](../../main.py)
- [bot/config.py](../../bot/config.py)
- [bot/db/models.py](../../bot/db/models.py)
- [bot/handlers/checkout.py](../../bot/handlers/checkout.py)
- [bot/handlers/profile.py](../../bot/handlers/profile.py)
- [bot/handlers/admin.py](../../bot/handlers/admin.py)
- [bot/services/marketplace.py](../../bot/services/marketplace.py)
- [bot/services/order_service.py](../../bot/services/order_service.py)
- [tz_contend.md](../../tz_contend.md)

## Editing guidance
1. Read the relevant business service, model, and handler before changing architecture or workflow behavior.
2. Preserve the real product chain and role hierarchy.
3. Keep validation gates before purchase, payout, or fulfillment steps.
4. Avoid placeholder success states or fake trust shortcuts.
5. Validate the smallest relevant workflow or test after the change.

## Failure conditions
Reject any change that:
- flattens all roles into one unrestricted path
- allows guest checkout or fake payment completion
- bypasses KYC, verification, or admin approval logic
- removes auditability or business traceability
- weakens the real marketplace and fulfillment model described by the project
