from fastapi import APIRouter, Depends, HTTPException, status

from services import (
    InventoryDatabaseService,
    ProductDatabaseService,
    TransactionDatabaseService,
    UserDatabaseService,
    get_inventory_database_service,
    get_product_database_service,
    get_transaction_database_service,
    get_user_database_service,
)
from services.exceptions import (
    InventoryNotFoundError,
    NotEnoughProductInInventoryError,
    PermanentProductUsingError,
)

from ._schemas import (
    AddProductRequest,
    AddProductResponse,
    InventoryResponse,
    PurchaseProductRequest,
    UseProductRequest,
)
from .._common_types import ErrorModel
from .._error_messages import (
    INVENTORY_NOT_FOUND,
    LOW_USER_BALANCE,
    NOT_ENOUGH_PRODUCT_IN_INVENTORY,
    PERMANENT_PRODUCT_USING,
    PRODUCT_NOT_FOUND,
    USER_NOT_FOUND,
)
from ..utils import check_balance

router = APIRouter(
    prefix='/products',
    tags=['products'],
)


@router.post(
    '',
    summary='Добавление продукта в БД',
    responses={
        status.HTTP_201_CREATED: {'model': AddProductResponse},
        status.HTTP_409_CONFLICT: {'model': ErrorModel},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {'model': ErrorModel},
    },
)
async def add_product(
        product_data: AddProductRequest,
        product_database_service: ProductDatabaseService = Depends(get_product_database_service),
) -> AddProductResponse:
    product = await product_database_service.add_product(**product_data.model_dump())
    return AddProductResponse.model_validate(
        product,
        from_attributes=True,
        by_alias=True,
    )


@router.post(
    '/{product_id}/purchase',
    summary='Покупка товара',
    responses={
        status.HTTP_200_OK: {'model': InventoryResponse},
        status.HTTP_404_NOT_FOUND: {'model': ErrorModel},
        status.HTTP_409_CONFLICT: {'model': ErrorModel},
        status.HTTP_422_UNPROCESSABLE_CONTENT: {'model': ErrorModel},
    },
)
async def purchase_product(
        product_id: int,
        puchase_product_data: PurchaseProductRequest,
        user_database_service: UserDatabaseService = Depends(get_user_database_service),
        product_database_service: ProductDatabaseService = Depends(get_product_database_service),
        transaction_database_service: TransactionDatabaseService = Depends(get_transaction_database_service),
) -> InventoryResponse:
    user = await user_database_service.get_by_id(user_id=puchase_product_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=USER_NOT_FOUND,
        )
    product = await product_database_service.get_by_id(product_id=product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=PRODUCT_NOT_FOUND,
        )
    difference, low_balance = check_balance(user.balance, product.price)
    if low_balance:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=LOW_USER_BALANCE.format(difference),
        )
    inventory = await transaction_database_service.purchase_product(user=user, product=product)
    return InventoryResponse.model_validate(
        inventory,
        from_attributes=True,
        by_alias=True,
    )


@router.post(
    '/{product_id}/use',
    summary='Использование consumable товара',
)
async def use_product(
    product_id: int,
    use_product_request: UseProductRequest,
    inventory_database_service: InventoryDatabaseService = Depends(get_inventory_database_service),
):
    try:
        inventory = await inventory_database_service.use_product(
            product_id=product_id,
            user_id=use_product_request.user_id,
        )
    except InventoryNotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=INVENTORY_NOT_FOUND)
    except PermanentProductUsingError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=PERMANENT_PRODUCT_USING)
    except NotEnoughProductInInventoryError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=NOT_ENOUGH_PRODUCT_IN_INVENTORY)
    return InventoryResponse.model_validate(
        inventory,
        from_attributes=True,
        by_alias=True,
    )
