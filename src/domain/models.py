from typing import Optional
from sqlmodel import Field, SQLModel

# Usamos SQLModel como base, pero en Clean Arch purista,
# esto sería una dataclass pura. SQLModel es un buen punto medio pragmático.

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: float
    stock: int
    barcode: str = Field(unique=True)
