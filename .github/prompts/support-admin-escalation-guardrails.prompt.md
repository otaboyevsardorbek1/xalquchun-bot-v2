# Support and admin escalation guardrails

## Role
You are reviewing or editing the support and moderation layer of a production Telegram commerce platform. This prompt applies to escalations, dispute handling, customer support workflows, moderator actions, approval decisions, and any administrative operation that affects platform trust or user safety.

## Non-negotiable rules
- Support and admin actions must never bypass authentication, blocked-user checks, verification gates, order validation, or financial safety checks.
- No fake resolution states, no silent account approval, no hidden privilege escalation, and no unauthorized balance or payout changes.
- Customer identity, address, passport, and delivery data must remain protected and minimized in all logs and responses.
- Escalations must retain evidence, actor identity, timeline, and business context.
- Real-world moderation and dispute processes must be auditable and reviewable.

## Business and data expectations
- Support workflows should document issue type, user identity, order or transaction linkage, and resolution path.
- Admin moderation must preserve clear approvals and consistent role boundaries.
- Platform trust actions, such as blocking, unblocking, verifying, or approving payouts, require explicit evidence and audit history.
- Support and moderation tools must not become a path to bypass the commerce rules of the XalqUchun ecosystem.

## Files to inspect first
- [main.py](../../main.py)
- [bot/db/models.py](../../bot/db/models.py)
- [bot/handlers/admin.py](../../bot/handlers/admin.py)
- [bot/handlers/profile.py](../../bot/handlers/profile.py)
- [bot/handlers/checkout.py](../../bot/handlers/checkout.py)
- [bot/services/audit.py](../../bot/services/audit.py)
- [tests/test_checkout_guardrails.py](../../tests/test_checkout_guardrails.py)

## Editing guidance
1. Read the relevant admin, audit, profile, and order logic before changing support or moderation behavior.
2. Preserve user verification, KYC, and order integrity gates.
3. Prefer explicit approval flows and audit log entries over implicit trust.
4. Keep support actions minimal, reviewable, and tied to user records.
5. Validate the smallest impacted workflow after the change.

## Failure conditions
Reject any change that:
- bypasses KYC, verification, or blocked-user enforcement
- allows fake dispute resolution, fake admin approval, or silent financial credit
- leaks personal or delivery data in support/admin messages or logs
- removes auditability from moderation or escalation events
- erodes the separation between customer, support, admin, and marketplace roles
