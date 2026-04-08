from fastapi import APIRouter, HTTPException, Query, Body
from typing import Optional, List
from api.services.books_service import BookService
from api.schemas.book_schema import BookCreate, BookUpdate, LocalCurrency, BookResponse
from api.schemas.api_response_schema import ApiResponse, PaginatedResponse

router = APIRouter(prefix="/api/v1")

books_service = BookService()

# ============================================================================================
#  >> Endpoint GET sin Paginacion
# --------------------------------------------------------------------------------------------

@router.get(
    "/books/all", 
    tags=["Vistas de Libros"], 
    summary="Obtener todos los libros",
    description="Retorna una lista completa de todos los libros registrados en la base de datos sin ningún tipo de filtrado o paginación. **Uso recomendado para reportes internos**.",
    response_model=ApiResponse[List[BookResponse]],
    responses={
    200: {"description": "Lista de libros encontrada exitosamente."},
    404: {"description": "No se encontraron libros."},
    500: {"description": "Error interno del servidor."}
})
async def get_books():
    return await books_service.get_books()

# ============================================================================================
#  >> Endpoints CRUD Básicos
# --------------------------------------------------------------------------------------------
@router.get(
    "/books", 
    tags=["CRUD de Libros"], 
    summary="Listar libros con paginación",
    description="Permite obtener un listado de libros de forma controlada mediante parámetros de página y límite. Ideal para visualización en aplicaciones frontend.",
    response_model=PaginatedResponse[List[BookResponse]],
    responses={
    200: {"description": "Lista de libros encontrada exitosamente."},
    404: {"description": "No se encontraron libros."},
    500: {"description": "Error interno del servidor."}
})
async def get_books_paginated(
    page: int = Query(0, ge=0, description="Número de página (comienza en 0)."),
    limit: int = Query(10, ge=1, description="Cantidad de elementos por página (mínimo 1).")
):
    return await books_service.get_books_paginated(page=page, limit=limit)


@router.post(
    "/books", 
    tags=["CRUD de Libros"], 
    summary="Registrar un nuevo libro",
    description="Crea un nuevo registro de libro en el sistema. Valida que el **ISBN** no esté duplicado antes de procesar la creación.",
    response_model=ApiResponse[BookResponse],
    responses={
    201: {"description": "Libro creado exitosamente."},
    409: {"description": "El libro con el ISBN proporcionado ya existe."},
    500: {"description": "Error interno del servidor."}
})
async def create_book(book: BookCreate = Body()):
    return await books_service.create_book(book)

# ============================================================================================
#  >> Endpoint Opcionales (Rutas específicas van primero)
# --------------------------------------------------------------------------------------------
@router.get(
    "/books/search/all", 
    tags=["Búsqueda e Inventario"], 
    summary="Búsqueda rápida por categoría",
    description="Realiza una búsqueda de libros filtrando por categoría de forma parcial (case-insensitive). Retorna todos los resultados sin paginación.",
    response_model=ApiResponse[List[BookResponse]],
    responses={
    200: {"description": "Libros encontrados exitosamente."},
    404: {"description": "No se encontraron libros con ese criterio."},
    500: {"description": "Error interno del servidor."}
})
async def search_books(category: Optional[str] = Query(None, description="Buscar libros por categoría (búsqueda parcial)")):
    return await books_service.search_books(category)


@router.get(
    "/books/low-stock/all", 
    tags=["Búsqueda e Inventario"], 
    summary="Listado completo de bajo stock",
    description="Identifica todos los libros cuyo stock actual es menor o igual al umbral (threshold) proporcionado. Útil para auditorías rápidas de inventario.",
    response_model=ApiResponse[List[BookResponse]],
    responses={
    200: {"description": "Libros encontrados exitosamente."},
    404: {"description": "No se encontraron libros con ese criterio."},
    500: {"description": "Error interno del servidor."}
})
async def low_stock_books(threshold: Optional[int] = Query(None, ge=0, description="Buscar libros de bajo stock.")):
    return await books_service.low_stock_books(threshold) 

# Versiones Paginadas

@router.get(
    "/books/search", 
    tags=["Búsqueda e Inventario"], 
    summary="Búsqueda paginada por categoría",
    description="Versión paginada de la búsqueda por categoría. Permite gestionar grandes volúmenes de resultados de búsqueda.",
    response_model=PaginatedResponse[List[BookResponse]],
    responses={
    200: {"description": "Libros encontrados exitosamente."},
    404: {"description": "No se encontraron libros con ese criterio."},
    500: {"description": "Error interno del servidor."}
})
async def search_books_paginated(
    category: Optional[str] = Query(None, description="Buscar libros por categoría (búsqueda parcial)"),
    page: int = Query(0, ge=0, description="Número de página (comienza en 0)."),
    limit: int = Query(10, ge=1, description="Cantidad de elementos por página (mínimo 1).")
):
    return await books_service.search_books_paginated(category, page=page, limit=limit)

@router.get(
    "/books/low-stock", 
    tags=["Búsqueda e Inventario"], 
    summary="Inventario bajo con paginación",
    description="Consulta paginada de libros con existencias limitadas. Los parámetros de página y límite son opcionales pero recomendados para el frontend.",
    response_model=PaginatedResponse[List[BookResponse]],
    responses={
    200: {"description": "Libros encontrados exitosamente."},
    404: {"description": "No se encontraron libros con ese criterio."},
    500: {"description": "Error interno del servidor."}
})
async def low_stock_books_paginated(
    threshold: Optional[int] = Query(None, ge=0, description="Buscar libros de bajo stock."),
    page: Optional[int] = Query(None, ge=0, description="Número de página (comienza en 0, opcional). Si no se especifica, se retornan todos los libros."),
    limit: Optional[int] = Query(None, ge=1, description="Cantidad de elementos por página (mínimo 1, opcional). Si no se especifica, se retornan todos los libros.")
):
    return await books_service.low_stock_books_paginated(threshold, page=page, limit=limit) 


# ============================================================================================
#  >> Endpoints CRUD Básicos

@router.get(
    "/books/{id}", 
    tags=["CRUD de Libros"], 
    summary="Consultar detalles de un libro",
    description="Obtiene toda la información detallada de un libro específico utilizando su ID único en la base de datos.",
    response_model=ApiResponse[BookResponse],
    responses={
    200: {"description": "Libro encontrado exitosamente."},
    404: {"description": "El libro con el ID proporcionado no existe."},
    500: {"description": "Error interno del servidor."}
})
async def get_book_by_id(id: int):
    return await books_service.get_book_by_id(id) 


@router.put(
    "/books/{id}", 
    tags=["CRUD de Libros"], 
    summary="Actualización parcial de libro",
    description="Permite modificar cualquier campo de un libro existente (título, autor, precio, etc.). No es necesario enviar el objeto completo, solo los campos a cambiar.",
    response_model=ApiResponse[BookResponse],
    responses={
    200: {"description": "Libro actualizado exitosamente."},
    404: {"description": "El libro con el ID proporcionado no existe."},
    409: {"description": "Conflicto, ya existe un libro con el mismo ISBN o título."},
    500: {"description": "Error interno del servidor."}
})
async def update_book_by_id(id: int, book: BookUpdate = Body()):
    return await books_service.update_book_by_id(id, book) 

@router.delete(
    "/books/{id}", 
    tags=["CRUD de Libros"], 
    summary="Dar de baja un libro",
    description="Elimina permanentemente el registro del libro del sistema de inventario.",
    response_model=ApiResponse,
    responses={
    200: {"description": "Libro eliminado exitosamente."},
    404: {"description": "El libro con el ID proporcionado no existe."},
    500: {"description": "Error interno del servidor."}
})
async def delete_book_by_id(id: int):
    return await books_service.delete_book_by_id(id) 


# ============================================================================================
#  >> Endpoint con Integración Externa (Importante)
# --------------------------------------------------------------------------------------------
@router.post(
    "/books/{id}/calculate-price", 
    tags=["Integraciones Externas"],
    summary="Simular cambio de divisa",
    description="Calcula cuánto costaría el libro en una moneda extranjera (EUR, MXN, etc.) basándose en el costo base en USD y tipos de cambio reales. Actualiza el precio local en la base de datos.",
    response_model=ApiResponse
) # la prueba decia que hiciera esto un post, pero lo veo mas como patch
async def calculate_book_price(id: int, currency_code: LocalCurrency = Body()):
    return await books_service.calculate_book_price(id, currency_code) 
