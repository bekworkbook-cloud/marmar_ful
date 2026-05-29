from src.core.domain.exceptions.validation import DomainValidationError

class Category:
    def __init__(
        self,
        id: int | None,
        name: str,
        description: str,
        branch_id: int,
        is_active: bool
    ):
        self.id = id
        self.name = name
        self.description = description
        self.branch_id = branch_id
        self.is_active = is_active

        if not name.strip():
            raise DomainValidationError("Category name cannot be empty")

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False


    def update_fields(self, name: str, description: str, branch_id: int, is_active: bool) -> None:
        self.name = name
        self.description = description
        self.branch_id = branch_id
        self.is_active = is_active

    