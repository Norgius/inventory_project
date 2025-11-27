import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.alias_generators import to_camel

from .._common_types import UserName


class RegisterUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=254)
    email: EmailStr

    model_config = ConfigDict(
        extra='forbid',
    )


class RegisterUserResponse(BaseModel):
    user_id: int = Field(validation_alias='id')
    username: UserName
    email: EmailStr
    balance: int
    created_at: datetime.datetime

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class AddFundsRequest(BaseModel):
    amount: int = Field(gt=0, le=1000000)

    model_config = ConfigDict(
        extra='forbid',
    )


class AddFundsResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    balance: int


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    type: str
    price: int
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )


class InventoryWithProductsResponse(BaseModel):
    id: int
    quantity: int | None
    purchased_at: datetime.datetime
    product: ProductResponse

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserResponse(BaseModel):
    id: int
    username: str
    email: str | None
    balance: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class GetInventoryResponse(BaseModel):
    user: UserResponse
    inventories: list[InventoryWithProductsResponse]
