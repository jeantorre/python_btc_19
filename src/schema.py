from typing import Union

from pydantic import BaseModel, PositiveFloat, PositiveInt


class ItemBase(BaseModel):
    nome: str
    preco: PositiveFloat
    em_oferta: Union[bool, None] = None


class CriarItem(ItemBase):
    pass


class Item(ItemBase):
    id: PositiveInt
