import pytest
from unittest.mock import AsyncMock, MagicMock

from src.shared.dto.category_dto import CategoryCreate, CategoryDTO
from src.infrastructure.database.models.category import Category as CategoryModel
from src.core.application.use_cases.post_category_use_case import PostCategoryUseCase

@pytest.mark.asyncio
async def test_post_category_use_case_success():
    mock_repo = MagicMock()
    mock_repo.add = AsyncMock()
    
    mock_returned_model = MagicMock()
    mock_returned_model.id = 1
    mock_returned_model.name = "Электроника"
    mock_returned_model.description = "Описание категории"
    mock_returned_model.branch_id = 12
    mock_returned_model.is_active = True
    mock_repo.add.return_value = mock_returned_model
    
    category_data = MagicMock()
    category_data.name = "Электроника"
    category_data.description = "Описание категории"
    category_data.branch_id = 12
    category_data.is_active = True
    
    use_case = PostCategoryUseCase(category_repo=mock_repo)
    result = await use_case.execute(category_data)
    
    assert result.id == 1
    assert result.name == "Электроника"
    assert result.description == "Описание категории"
    assert result.branch_id == 12
    assert result.is_active is True
    
    mock_repo.add.assert_called_once()
    passed_model = mock_repo.add.call_args.kwargs['category']
    assert passed_model.name == "Электроника"
    assert passed_model.description == "Описание категории"
    assert passed_model.branch_id == 12
    assert passed_model.is_active is True