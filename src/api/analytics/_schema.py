from pydantic import BaseModel, ConfigDict

from orm.models import ProductType


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: int
    type: ProductType
    is_active: bool
    purchase_count: int

    model_config = ConfigDict(
        from_attributes=True,
    )
