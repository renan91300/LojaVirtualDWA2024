from pydantic import BaseModel, field_validator

from util.validators import *


class ExcluirProdutoDTO(BaseModel):
    id: int

    @field_validator("id")
    def validar_id(cls, v):
        msg = is_greater_than(v, "id", 0)
        if msg:
            raise ValueError(msg)
        return v