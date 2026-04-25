from src.infrastructure.database.models.category import Category

from src.infrastructure.database.dao.base import BaseDAO

class CategoryDAO(BaseDAO):
    model = Category

    