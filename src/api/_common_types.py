from typing import Annotated, Any

from pydantic import BaseModel, StringConstraints

from orm.models import USERNAME_MAX_LENGTH

UserName = Annotated[
    str,
    StringConstraints(max_length=USERNAME_MAX_LENGTH),
]


class ErrorModel(BaseModel):
    detail: str | dict[str, Any]
