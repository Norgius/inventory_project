import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from orm.models import ProductType, TransactionStatus


class PurchaseProductRequest(BaseModel):
    user_id: int
    """ID пользователя"""

    model_config = ConfigDict(
        use_attribute_docstrings=True,
        extra='forbid',
    )


class AddProductRequest(BaseModel):
    name: str = Field(max_length=254)
    description: str | None = None
    price: PositiveInt
    product_type: ProductType = Field(alias='type')

    model_config = ConfigDict(
        use_attribute_docstrings=True,
        extra='forbid',
    )


class AddProductResponse(BaseModel):
    id: int
    name: str = Field(max_length=254)
    description: str | None = None
    price: PositiveInt
    type: ProductType

    model_config = ConfigDict(
        use_attribute_docstrings=True,
    )


class InventoryResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int | None
    purchased_at: datetime.datetime


class PurchaseProductResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    amount: int
    status: TransactionStatus
    created_at: datetime.datetime


class UseProductRequest(BaseModel):
    user_id: int

    model_config = ConfigDict(
        use_attribute_docstrings=True,
        extra='forbid',
    )
