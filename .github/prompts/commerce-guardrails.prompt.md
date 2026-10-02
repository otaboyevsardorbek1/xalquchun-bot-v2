# Commerce guardrails prompt

## Role
You are working on a production-grade Telegram commerce bot. Every change must preserve user safety, identity verification, transaction integrity, and business compliance.

## Mandatory rules
- Guests must never reach checkout, payment, or order placement flows.
- Users must complete registration before purchasing.
- Required profile data includes full name, phone number, delivery address, and identity data such as ID card or passport details.
- Only verified users may place orders and proceed through purchase steps.
- If verification is incomplete, request the missing information and block the shortcut path.
- Never bypass authentication, blocked-user checks, maintenance mode, or role authorization.
- Never expose raw personal data in logs, errors, public messages, or admin output.
- Treat payment and delivery flows as real operational business integrations, not fake success states.
- Prefer provider adapters and clear audit trails over placeholder fulfillment logic.
- Admin actions must remain auditable and must not bypass KYC or order validation.

## Business expectations
- Orders must be linked to the authenticated user and valid delivery data.
- Transactions must be linked to user identity and retain status history.
- Referral, balance, payout, and bonus logic must remain consistent and non-exploitative.
- Marketplace-style shipping and order fulfillment must reflect realistic status transitions and verification checks.

## When editing code
- Read the relevant handler and persistence model before changing behavior.
- Preserve the existing user verification and checkout guardrails.
- Keep config values in environment variables instead of hard-coded secrets or IDs.
- Validate the smallest specific workflow impacted by the change.

## Failure to comply
Do not introduce shortcuts that skip verification, guest blocking, order validation, or payment integrity checks.
