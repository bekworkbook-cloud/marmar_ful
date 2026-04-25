from src.core.domain.exceptions.validation import DomainValidationError

class Category:
    def __init__(
        self,
        id: int | None,
        name: str,
        desc: str,
        branch_id: int,
        is_active: bool
    ):
        if not name.strip():
            raise DomainValidationError("Category name cannot be empty")

        self.id = id
        self.name = name
        self.desc = desc
        self.branch_id = branch_id
        self.is_active = is_active

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False