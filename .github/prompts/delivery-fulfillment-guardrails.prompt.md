# Delivery and fulfillment guardrails

## Role
You are working on the logistics and fulfillment side of a production Telegram commerce platform. This prompt applies to delivery assignment, order status changes, location tracking, courier flow, fulfillment approval, and any action that affects customer trust or order completion.

## Non-negotiable rules
- Delivery and fulfillment must remain linked to a real verified customer and a valid order.
- No fake delivery confirmation, fake shipment state, or shortcut around order validation.
- Courier, vendor, admin, and customer roles must stay clearly separated.
- Orders must retain delivery data, contact number, status history, and user identity.
- If required data is missing or the user is unverified, block the live fulfillment path.
- Never expose raw personal data, addresses, or location details in logs, public messages, or admin output.
- Real delivery integration must be treated as a provider-style workflow, not a placeholder state.

## Business and data expectations
- Order status should move through realistic states such as new → processing → ready → delivered or cancelled.
- Fulfillment actions must be auditable and associated with the correct user or operator.
- Location data may be used for routing and delivery confirmation, but it must be handled with privacy safeguards.
- Marketplace roles remain distinct: customer, courier, vendor, dealer, developer, support, admin, super admin.

## Files to inspect first
- [main.py](../../main.py)
- [bot/db/models.py](../../bot/db/models.py)
- [bot/handlers/checkout.py](../../bot/handlers/checkout.py)
- [bot/handlers/admin.py](../../bot/handlers/admin.py)
- [bot/handlers/profile.py](../../bot/handlers/profile.py)
- [bot/services/order_service.py](../../bot/services/order_service.py)
- [tests/test_checkout_guardrails.py](../../tests/test_checkout_guardrails.py)

## Editing guidance
1. Read the relevant order, checkout, and admin logic before changing delivery behavior.
2. Preserve the user verification and order integrity gates before fulfillment proceeds.
3. Keep status transitions explicit and traceable.
4. Prefer provider-style adapters and explicit audit logging over placeholder logic.
5. Validate the smallest impacted workflow after the change.

## Failure conditions
Reject any change that:
- allows fake completion or “delivered” without real confirmation
- bypasses verification or role checks for courier/vendor/admin operations
- leaks personal delivery data into logs or public messages
- drops status history or order traceability
- weakens the real marketplace chain: Developer Partner → Dealer → Vendor → Customer → Courier
