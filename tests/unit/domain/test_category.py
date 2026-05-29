import pytest

from src.core.domain.entities.category import Category, DomainValidationError


def test_category():

    category = Category(
        id=1,
        name="Bar",
        description="BarDesc",
        branch_id=1,
        is_active=True
    )

    assert category.id == 1
    assert category.name == "Bar"
    assert category.description == "BarDesc"
    assert category.branch_id == 1
    assert category.is_active == True


