from typing import Any
from pydantic import EmailStr, ValidationError

def validate_email(email: str) -> EmailStr:
    """Validate that a string is a proper email address.
    Raises:
        ValueError: If the email is invalid.
    """
    try:
        return EmailStr.validate(email)
    except ValidationError as exc:
        raise ValueError(str(exc))

def validate_sensitivity(level: str) -> str:
    """Validate sensitivity level.
    Returns the normalized level (lowercase).
    Raises:
        ValueError: If level is not one of low/medium/high.
    """
    allowed = {'low', 'medium', 'high'}
    low = level.lower()
    if low not in allowed:
        raise ValueError(f"Sensitivity must be one of {allowed}, got '{level}'.")
    return low
