from src.core.domain.exceptions.validation import DomainValidationError

class Branch:
    def __init__(
        self,
        id: int | None,
        name: str,
        branch_code: str,
        address: str,
        landmark: str,
        latitude: float,
        longitude: float,
        is_active: bool
    ):
        if not (-90.0 <= latitude <= 90.0):
            raise DomainValidationError("Latitude must be between -90 and 90 degrees")
        
        if not (-180.0 <= longitude <= 180.0):
            raise DomainValidationError("Longitude must be between -180 and 180 degrees")

        self.id = id
        self.name = name
        self.branch_code = branch_code
        self.address = address
        self.landmark = landmark
        self.latitude = latitude
        self.longitude = longitude
        self.is_active = is_active

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False