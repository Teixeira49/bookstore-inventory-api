from pydantic import BaseModel, Field
from typing import TypeVar, Generic, List, Optional

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    status_code: int = Field(..., example=200)
    detail: str = Field(..., example="Operación realizada con éxito")
    data: Optional[T] = None

    class Config:
        json_schema_extra = {
            "example": {
                "status_code": 200,
                "detail": "Libro encontrado exitosamente",
                "data": {
                    "id": 1,
                    "title": "El Quijote",
                    "author": "Miguel de Cervantes",
                    "isbn": "978-3-16-148410-0",
                    "stock_quantity": 50,
                    "cost_usd": 25.50
                }
            }
        }

class PaginatedResponse(ApiResponse, Generic[T]):
    limit: int = Field(..., example=10)
    page_number: int = Field(..., example=1)
    page_index: int = Field(..., example=0)
    page_size: int = Field(..., example=5)
    total_items: int = Field(..., example=100)
    total_pages: int = Field(..., example=10)
    is_first_page: bool = Field(..., example=True)
    is_last_page: bool = Field(..., example=False)

    class Config:
        json_schema_extra = {
            "example": {
                "status_code": 200,
                "detail": "Lista de libros cargada",
                "data": [
                    {"id": 1, "title": "Libro 1", "author": "Autor A", "isbn": "ISBN1"},
                    {"id": 2, "title": "Libro 2", "author": "Autor B", "isbn": "ISBN2"}
                ],
                "limit": 10,
                "page_number": 1,
                "page_index": 0,
                "page_size": 2,
                "total_items": 100,
                "total_pages": 10,
                "is_first_page": True,
                "is_last_page": False
            }
        }
