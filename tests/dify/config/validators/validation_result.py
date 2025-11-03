from typing import List
from dataclasses import dataclass


@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def error_count(self) -> int:
        return len(self.errors)

    def add_error(self, error: str) -> None:
        self.errors.append(error)
        self.is_valid = False

    def add_errors(self, errors: List[str]) -> None:
        self.errors.extend(errors)
        if errors:
            self.is_valid = False

    @classmethod
    def success(cls) -> "ValidationResult":
        return cls(is_valid=True, errors=[])

    @classmethod
    def failure(cls, errors: List[str]) -> "ValidationResult":
        return cls(is_valid=False, errors=errors)
