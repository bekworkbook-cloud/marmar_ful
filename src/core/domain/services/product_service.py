
from src.core.domain.entities.product import Product


class ProductService:

    def filter_by_branch(self, products: list[Product], branch_id: int):
        return [p for p in products if p.branch_id == branch_id]

    def calculate_discount(self, product: Product, percent: int):
        return product.price * (1 - percent / 100)