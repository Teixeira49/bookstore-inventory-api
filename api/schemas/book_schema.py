from pydantic import BaseModel, Field
from typing import Optional

class BookBase(BaseModel):
    """Esquema base con campos comunes."""
    title: str
    author: Optional[str] = None
    isbn: str = Field(..., description="ISBN debe ser único para cada libro.")
    cost_usd: float = Field(..., gt=0, description="El costo debe ser mayor que cero.")
    stock_quantity: int = Field(..., ge=0)
    category: Optional[str] = None
    supplier_country: Optional[str] = None

class BookCreate(BookBase):
    """Esquema para la creación de un libro. No se necesita más nada por ahora."""
    pass


class BookUpdate(BaseModel):
    """Esquema base con campos comunes."""
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    cost_usd: Optional[float] = None
    stock_quantity: Optional[int] = None
    category: Optional[str] = None
    supplier_country: Optional[str] = None

class LocalCurrency(BaseModel):
    currency_code: str = Field(..., gt=0, description="Debe contener algun codigo valido")

class Config:
    orm_mode = True