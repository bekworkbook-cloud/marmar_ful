import pytest

from src.core.domain.entities.branch import Branch, DomainValidationError


def test_branch_correct_test():

    latitude = 41.31123214521312
    longitude = 69.23982068205171

    branch = Branch(
        id=1,
        name="Drujba",
        description="Drujba description",
        branch_code="drujba",
        address="drujba 34",
        delivery_price=12000,
        landmark="Metro Drujba",
        latitude=latitude,
        longitude=longitude,
        is_active=True
    )

    assert branch.id == 1
    assert branch.name == "Drujba"
    assert branch.description == "Drujba description"
    assert branch.branch_code == "drujba"
    assert branch.delivery_price == 12000
    assert branch.address == "drujba 34"
    assert branch.landmark == "Metro Drujba"
    assert branch.latitude == latitude
    assert branch.longitude == longitude


def test_branch_wrong_longitude():

    latitude = 41.31123214521312
    longitude = 199.23982068205171

    with pytest.raises(DomainValidationError) as exc_info:

        branch = Branch(
            id=1,
            name="Drujba",
            branch_code="drujba",
            description="Drujba description",
            address="drujba 34",
            delivery_price=12000,
            landmark="Metro Drujba",
            latitude=latitude,
            longitude=longitude,
            is_active=True
        )

    assert str(exc_info.value) == "Longitude must be between -180 and 180 degrees"


def test_branch_wrong_latitude():
    latitude = 141.31123214521312
    longitude = 69.23982068205171

    with pytest.raises(DomainValidationError) as exc_info:
        branch = Branch(
            id=1,
            name="Drujba",
            description="Drujba description",
            branch_code="drujba",
            delivery_price=12000,
            address="drujba 34",
            landmark="Metro Drujba",
            latitude=latitude,
            longitude=longitude,
            is_active=True
        )

    assert str(exc_info.value) == "Latitude must be between -90 and 90 degrees"
