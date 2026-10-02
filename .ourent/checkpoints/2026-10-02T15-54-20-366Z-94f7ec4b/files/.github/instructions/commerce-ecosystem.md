# Commerce ecosystem guardrails

## Project model
This project follows the XalqUchun marketplace pattern described in [tz_contend.md](../../tz_contend.md): a multi-role commerce ecosystem with a shared backend, browser panels, Telegram bot navigation, and real-time order delivery.

Core chain:

Developer Partner -> Dealer -> Vendor -> Customer -> Courier

The platform is designed to support a marketplace that is not only a storefront, but also a logistics, fulfillment, payout, and verification network.

## Roles and responsibilities
### Customer
- Browses catalog and shops from vendor stores
- Places orders only after registration and verification
- Tracks order status and delivery
- Uses wallet, referral, and support tools

### Courier
- Accepts orders, follows route, reports location and delivery confirmation
- Must operate under verified status and active assignment rules
- Needs payout and performance tracking

### Vendor
- Manages catalog, inventory, pricing, orders, and payout requests
- Owns store operations and fulfillment coordination

### Dealer
- Manages a network of vendors or stores
- Supplies products and tracks commissions and performance
- Coordinates product distribution and support

### Developer Partner
- Produces the product offering or brand content
- Enters agreements with dealers and vendors
- Earns royalty revenue and monitors product quality

### Admin / Super Admin
- Reviews user KYC, store moderation, payouts, disputes, and audits
- Must protect platform trust, financial integrity, and compliance

### Support
- Handles user complaints, delivery issues, and communication escalations

## Required execution rules
- No guest checkout is allowed.
- Registration is required before a purchase is initiated.
- Required user data includes full name, phone number, delivery address, and ID/passport data.
- Only verified users may buy products or access the checkout flow.
- Unverified users must be directed back to profile completion instead of being allowed through a shortcut.
- Orders must store delivery details, contact info, status transitions, and user identity.
- Transaction records must include user linkage and financial type: payment, payout, bonus, refund, or manual adjustment.
- The system must treat payment and delivery as real operational flows, not fake success states.

## Architecture direction
- Frontend panels run in browser-based interfaces with Telegram bot integration.
- The backend is asynchronous and should support API, queue, cache, and real-time event flows.
- PostgreSQL stores canonical business records, while Redis is used for caching and real-time coordination.
- WebSocket events and status changes should be auditable and correlated with order IDs and user records.
- Provider adapters should represent external systems like payment gateways, SMS, maps, and logistics services.

## Financial model
- Every monetary movement must be linked to a real user and business context.
- Commission, payout, bonus, and refund logic must be transparent and auditable.
- Platform-level financial controls must exist for payout approval and dispute handling.
- No logic may silently create balance or credit without a traceable business reason.

## Security model
- Validate phone, address, and identity fields before allowing live order flows.
- Keep sensitive data encrypted or minimally stored, with access restricted by role.
- Support and admin tools must keep audit logs for key actions.
- Any message or report that includes personal data must be sanitized and minimized.

## Development guidance
When implementing features:
1. Read the relevant admin, checkout, order, and profile logic before editing.
2. Preserve verification, identity, and flow gating.
3. Prefer explicit service boundaries over shortcut logic.
4. Keep code aligned with the real commerce lifecycle: listing → cart → verification → checkout → payment → fulfillment → settlement.
5. Validate changes using the smallest relevant runtime or test check.

## Acceptance standard
A change is not acceptable if it weakens the no-guest rule, bypasses verification, masks payment completion, removes auditability, or treats a real marketplace flow as a fake placeholder.
