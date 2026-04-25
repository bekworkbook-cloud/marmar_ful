from src.infrastructure.database.models.payment_log import PaymentLog 

from src.infrastructure.database.dao.base import BaseDAO

class PaymentLogDAO(BaseDAO):
    model = PaymentLog

