from src.infrastructure.database.models.product import Product

from src.infrastructure.database.dao.base import BaseDAO

class ProductDAO(BaseDAO):
    model = Product

    