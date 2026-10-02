from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class KYCSubmission:
    full_name: str
    phone_number: str
    address: str
    passport_number: str
    id_document_data: str


class KYCService:
    """Real KYC workflow for verified commerce users."""

    @staticmethod
    def validate_submission(submission: KYCSubmission) -> Dict[str, Any]:
        errors = []

        if not submission.full_name or not submission.full_name.strip():
            errors.append("full_name")
        if not submission.phone_number or len(submission.phone_number.strip()) < 9:
            errors.append("phone_number")
        if not submission.address or not submission.address.strip():
            errors.append("address")
        if not submission.passport_number or not submission.passport_number.strip():
            errors.append("passport_number")
        if not submission.id_document_data or not submission.id_document_data.strip():
            errors.append("id_document_data")

        return {
            "allowed": not errors,
            "errors": errors,
        }

    @staticmethod
    def to_user_payload(submission: KYCSubmission) -> Dict[str, str]:
        return {
            "full_name": submission.full_name.strip(),
            "phone_number": submission.phone_number.strip(),
            "address": submission.address.strip(),
            "passport_number": submission.passport_number.strip(),
            "id_document_data": submission.id_document_data.strip(),
        }
