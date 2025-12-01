from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status

from app_context import limiter_var
from env_settings import settings
from services import (
    InventoryDatabaseService,
    UserDatabaseService,
    get_inventory_database_service,
    get_user_database_service,
)
from services.exceptions import UserAlreadyExistsError

from ._schemas import (
    AddFundsRequest,
    AddFundsResponse,
    GetInventoryResponse,
    InventoryWithProductsResponse,
    RegisterUserRequest,
    RegisterUserResponse,
    UserResponse,
)
from .._common_types import ErrorModel
from .._decorators import idempotent
from .._error_messages import USER_ALREADY_EXISTS, USER_NOT_FOUND

router = APIRouter(
    prefix='/users',
    tags=['users'],
)

limiter = limiter_var.get()


@router.post(
    '/register',
    summary='Регистрация пользователя',
    responses={
        status.HTTP_201_CREATED: {'model': RegisterUserResponse},
        status.HTTP_409_CONFLICT: {'model': ErrorModel},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {'model': ErrorModel},
        status.HTTP_429_TOO_MANY_REQUESTS: {'model': ErrorModel},
    },
)
@limiter.limit('10/minute')
async def register(
    request: Request,
    register_data: RegisterUserRequest,
    user_database_service: UserDatabaseService = Depends(get_user_database_service),
):
    try:
        user = await user_database_service.create(register_data.username, register_data.email)
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=USER_ALREADY_EXISTS,
        )
    return RegisterUserResponse.model_validate(
        user,
        from_attributes=True,
        by_alias=True,
    )


@router.post(
    '/{user_id}/add-funds',
    summary='Пополняет счёт пользователя',
    responses={
        status.HTTP_200_OK: {'model': None},
        status.HTTP_400_BAD_REQUEST: {'model': ErrorModel},
        status.HTTP_404_NOT_FOUND: {'model': ErrorModel},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {'model': ErrorModel},
        status.HTTP_429_TOO_MANY_REQUESTS: {'model': ErrorModel},
    },
)
@idempotent(
    expire=settings.CACHE_CONFIG.IDEMPOTENTY_TIMER,
    namespace=settings.CACHE_CONFIG.NAMESPACE.ADD_FUNDS,
)
async def add_funds(
    request: Request,
    user_id: int,
    add_funds_request: AddFundsRequest,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", convert_underscores=False)],
    user_database_service: UserDatabaseService = Depends(get_user_database_service),
) -> AddFundsResponse:
    user = await user_database_service.get_by_id(user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=USER_NOT_FOUND,
        )
    user = await user_database_service.add_funds(user=user, amount=add_funds_request.amount)
    return AddFundsResponse.model_validate(
        user,
        from_attributes=True,
        by_alias=True,
    )


@router.get(
    '/{user_id}/add-funds',
    summary='Получение полного инвентаря пользователя',
    responses={
        status.HTTP_200_OK: {'model': GetInventoryResponse},
        status.HTTP_404_NOT_FOUND: {'model': ErrorModel},
    },
)
async def get_inventory(
    user_id: int,
    user_database_service: UserDatabaseService = Depends(get_user_database_service),
    inventory_database_service: InventoryDatabaseService = Depends(get_inventory_database_service),
):
    user = await user_database_service.get_by_id(user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=USER_NOT_FOUND,
        )
    inventories = await inventory_database_service.get_user_inventories(user_id=user_id)
    return GetInventoryResponse(
        user=UserResponse.model_validate(user),
        inventories=[InventoryWithProductsResponse.model_validate(inv) for inv in inventories],
    )
