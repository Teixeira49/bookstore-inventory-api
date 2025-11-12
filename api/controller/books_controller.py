from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import Field
from typing import Optional
from api.models.book import Book
from api.services.books_service import BookService
from api.schemas.book_schema import BookCreate, BookUpdate, LocalCurrency

router = APIRouter(prefix="/api")

books_service = BookService()

# ============================================================================================
#  >> Endpoint GET sin Paginacion
# --------------------------------------------------------------------------------------------

@router.get("/books/all", responses={
    200: {"description": "Lista de libros encontrada exitosamente."},
    404: {"description": "No se encontraron libros."},
    500: {"description": "Error interno del servidor."}
})
async def get_books():
    return await books_service.get_books()

# ============================================================================================
#  >> Endpoints CRUD Básicos
# --------------------------------------------------------------------------------------------
@router.get("/books", responses={
    200: {"description": "Lista de libros encontrada exitosamente."},
    404: {"description": "No se encontraron libros."},
    500: {"description": "Error interno del servidor."}
})
async def get_books_paginated(skip: int = 0, limit: int = 10):
    return await books_service.get_books_paginated(skip=skip, limit=limit)


@router.post("/books", responses={
    201: {"description": "Libro creado exitosamente."},
    409: {"description": "El libro con el ISBN proporcionado ya existe."},
    500: {"description": "Error interno del servidor."}
})
async def create_book(book: BookCreate = Body()):
    return await books_service.create_book(book)

# ============================================================================================
#  >> Endpoint Opcionales (Rutas específicas van primero)
# --------------------------------------------------------------------------------------------
@router.get("/books/search", responses={
    200: {"description": "Libros encontrados exitosamente."},
    404: {"description": "No se encontraron libros con ese criterio."},
    500: {"description": "Error interno del servidor."}
})
async def search_books(category: Optional[str] = Query(None, description="Buscar libros por categoría (búsqueda parcial)")):
    return await books_service.search_books(category)

# ============================================================================================
#  >> Endpoints CRUD Básicos

@router.get("/books/{id}", responses={
    200: {"description": "Libro encontrado exitosamente."},
    404: {"description": "El libro con el ID proporcionado no existe."},
    500: {"description": "Error interno del servidor."}
})
async def get_book_by_id(id: int):
    return await books_service.get_book_by_id(id) 


@router.put("/books/{id}", responses={
    200: {"description": "Libro actualizado exitosamente."},
    404: {"description": "El libro con el ID proporcionado no existe."},
    409: {"description": "Conflicto, ya existe un libro con el mismo ISBN o título."},
    500: {"description": "Error interno del servidor."}
})
async def update_book_by_id(id: int, book: BookUpdate = Body()):
    return await books_service.update_book_by_id(id, book) 

@router.delete("/books/{id}", responses={
    200: {"description": "Libro eliminado exitosamente."},
    404: {"description": "El libro con el ID proporcionado no existe."},
    500: {"description": "Error interno del servidor."}
})
async def delete_book_by_id(id: int):
    return await books_service.delete_book_by_id(id) 


# ============================================================================================
#  >> Endpoint con Integración Externa (Importante)
# --------------------------------------------------------------------------------------------
@router.post("/books/{id}/calculate-price") # la prueba decia que hiciera esto un post, pero lo veo mas como patch
async def calculate_book_price(id: int, currency_code: LocalCurrency = Body()):
    return await books_service.calculate_book_price(id, currency_code) 


"""
@router.get("/books/low-stock")
async def low_stock_books():
    try:
        exchange_rate = await books_service.low_stock_books() 
        return {"exchange_rate": exchange_rate}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""