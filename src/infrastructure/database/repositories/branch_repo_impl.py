from src.core.domain.interfaces.branch_repo import BranchRepository
from src.core.domain.entities.branch import Branch
from src.infrastructure.database.models.branch import Branch as BranchModel
from src.infrastructure.database.dao.branch_dao import BranchDAO

class BranchRepositoryImpl(BranchRepository):
    def __init__(self, branch_dao: BranchDAO):
        self.branch_dao = branch_dao

    def _to_entity(self, model: BranchModel) -> Branch:
        return Branch(
            id=model.id,
            name=model.name,
            branch_code=model.branch_code,
            description=model.description,
            address=model.address,
            landmark=model.landmark,
            latitude=model.latitude,
            longitude=model.longitude,
            delivery_price=model.delivery_price,
            is_active=model.is_active
        )

    def _to_model(self, entity: Branch) -> BranchModel:
        return BranchModel(
            id=entity.id,
            name=entity.name,
            branch_code=entity.branch_code,
            description=entity.description,
            address=entity.address,
            landmark=entity.landmark,
            latitude=entity.latitude,
            longitude=entity.longitude,
            delivery_price=entity.delivery_price,
            is_active=entity.is_active
        )

    async def add(self, branch: Branch) -> Branch:
        branch_model = self._to_model(branch)
        created_model = await self.branch_dao.add(branch_model)
        return self._to_entity(created_model)
    
    async def get_by_id(self, branch_id: int) -> Branch:
        model = await self.branch_dao.get_by_id(branch_id)
        return self._to_entity(model)
    
    async def get_all(self) -> list[Branch]:
        models = await self.branch_dao.get_all()
        return [self._to_entity(model) for model in models]

    async def update(self, branch: Branch) -> Branch:
        branch_model = self._to_model(branch)
        updated_model = await self.branch_dao.update(branch_model)
        return self._to_entity(updated_model)

    async def delete(self, branch_id: int) -> None:
        return await self.branch_dao.delete(branch_id)

    async def get_list(self, limit: int = 10, offset: int = 0, **filters) -> list[Branch]:
        models = await self.branch_dao.get_list(limit=limit, offset=offset, **filters)
        return [self._to_entity(model) for model in models]
    