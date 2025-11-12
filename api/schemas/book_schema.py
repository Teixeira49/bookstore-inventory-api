from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class BookBase(BaseModel):
    """Esquema base con campos comunes."""
    title: str = Field(..., min_length=1, max_length=255, description="Título del libro, no puede estar vacío.")
    author: Optional[str] = None
    isbn: str = Field(..., description="ISBN debe ser único y tener 10 o 13 dígitos.")
    cost_usd: float = Field(..., gt=0, description="El costo debe ser mayor que cero.")
    stock_quantity: int = Field(..., ge=0)
    category: Optional[str] = None
    supplier_country: Optional[str] = None

    @field_validator('isbn')
    def validate_isbn(cls, v):
        """Valida que el ISBN tenga 10 o 13 dígitos y solo contenga números, guiones y opcionalmente una 'X'."""
        if not re.match(r'^[0-9-X]+$', v, re.IGNORECASE):
            raise ValueError('El ISBN solo puede contener números, guiones y, opcionalmente, una "X".')
        
        cleaned_isbn = v.replace('-', '')
        if not (len(cleaned_isbn) == 10 or len(cleaned_isbn) == 13):
            raise ValueError('El ISBN debe tener 10 o 13 dígitos (sin contar guiones).')
        return v
    
    @field_validator('cost_usd')
    def cost_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El costo debe ser mayor que cero.')
        return v

    @field_validator('stock_quantity')
    def stock_must_be_non_negative(cls, v):
        if v is not None and v < 0:
            raise ValueError('El stock no puede ser negativo.')
        return v

class BookCreate(BookBase):
    """Esquema para la creación de un libro. No se necesita más nada por ahora."""
    pass


class BookUpdate(BaseModel):
    """
    Esquema para actualizar un libro. Todos los campos son opcionales.
    Las validaciones de BookBase se aplican si los campos están presentes.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Título del libro, no puede estar vacío.")
    author: Optional[str] = None
    isbn: Optional[str] = Field(None, description="ISBN debe ser único y tener 10 o 13 dígitos (sin contar guiones).")
    cost_usd: Optional[float] = None
    stock_quantity: Optional[int] = None
    category: Optional[str] = None
    supplier_country: Optional[str] = None

    @field_validator('title')
    def check_not_empty(cls, v, field):
        if v is not None and not str(v).strip():
            raise ValueError(f'El campo {field.name} no puede estar vacío o contener solo espacios.')
        return v

class LocalCurrency(BaseModel):
    code: str = Field(..., description="Debe contener algun codigo valido")
    
    @field_validator('code')
    def code_must_be_uppercase(cls, v):
        return v.upper()

class Config:
    orm_mode = True