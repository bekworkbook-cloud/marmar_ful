from src.core.application.exceptions.not_found_exception import NotFoundException
from src.core.domain.interfaces.product_repo import ProductRepository
from src.core.application.use_cases.dtos.product_dtos import ProductDTO

class DeleteProductUseCase:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def execute(self, product_id: int) -> None:
        return await self.product_repo.delete(product_id=product_id)
        