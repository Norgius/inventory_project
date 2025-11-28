class UserAlreadyExistsError(Exception):
    pass


class InventoryNotFoundError(Exception):
    pass


class PermanentProductUsingError(Exception):
    pass


class NotEnoughProductInInventoryError(Exception):
    pass


class PurchaseProductError(Exception):
    pass
