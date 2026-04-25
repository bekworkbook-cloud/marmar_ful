from pydantic import BaseModel


class CartAddSchema(BaseModel):
    branch_id: str
    category_id: int | str
    product_id: int
    product_price_at_purchase: int
    quantity: int
    init_data: str = ""
