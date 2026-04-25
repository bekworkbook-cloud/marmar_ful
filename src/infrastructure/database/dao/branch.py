from src.infrastructure.database.models.branch import Branch
from src.infrastructure.database.dao.base import BaseDAO

class BranchDAO(BaseDAO):
    model = Branch

