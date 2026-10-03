# Role-boundary and marketplace chain guardrails

## Role
You are reviewing or editing a production Telegram commerce platform whose business model follows the XalqUchun chain: Developer Partner → Dealer → Vendor → Customer → Courier. This prompt applies to any feature that touches role permissions, access boundaries, marketplace logic, or business actor separation.

## Non-negotiable rules
- Role boundaries must remain explicit and enforced.
- Customer, courier, vendor, dealer, developer partner, support, admin, and super admin are different operating roles and must not share unrestricted privileges.
- No user may bypass role checks, verification gates, or order validation through a cross-role shortcut.
- Marketplace flows must stay consistent with the real chain and business logic.
- No fake access grant, fake approval, or fake marketplace action.
- Personal data, delivery data, and identity information must remain protected and minimized in logs and user-facing messages.

## Business and data expectations
- Orders, payments, payouts, referrals, and audit records must always remain tied to the correct user and role.
- Permissions must be explicit, not inferred from a generic bot state.
- Admin and support tools must preserve accountability, traceability, and approval evidence.
- Multi-role operations must follow clear boundaries instead of a single unrestricted admin path.

## Files to inspect first
- [main.py](../../main.py)
- [bot/db/models.py](../../bot/db/models.py)
- [bot/handlers/admin.py](../../bot/handlers/admin.py)
- [bot/handlers/checkout.py](../../bot/handlers/checkout.py)
- [bot/handlers/profile.py](../../bot/handlers/profile.py)
- [bot/services/marketplace.py](../../bot/services/marketplace.py)
- [tests/test_checkout_guardrails.py](../../tests/test_checkout_guardrails.py)

## Editing guidance
1. Read the relevant role policy, order flow, and admin logic before changing access or marketplace behavior.
2. Preserve the real chain and business boundaries instead of flattening all roles into a single admin-like user.
3. Keep approvals, role checks, and audit records explicit.
4. Prefer small, reviewable policy checks over broad “if user is logged in” shortcuts.
5. Validate the smallest affected workflow after the change.

## Failure conditions
Reject any change that:
- collapses distinct roles into one unrestricted access level
- bypasses verification or customer purchase gates
- introduces fake marketplace approval, payout, or fulfillment states
- destroys auditability or role traceability
- weakens the XalqUchun chain and real business model
