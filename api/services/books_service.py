from typing import Optional
from fastapi import HTTPException

from api.services.database_service import *
from api.schemas.book_schema import BookCreate, BookUpdate
from api.models.book import Book
from api.utils.response_wrapper import api_response

class BookService:
    def __init__(self):
        pass

# --------------------------------------------------------------------
# #  >> Servicios para Endpoints CRUD Básicos

    async def get_books(self):
        try:
            books = get_books_to_db()
            if not books:
                raise HTTPException(status_code=404, detail="No se encontraron libros.")
            return api_response(data=books)
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def create_book(self, book_data: BookCreate):
        try:
            existing_book = find_book_by_isbn_to_db(book_data.isbn)
            if existing_book:
                raise HTTPException(status_code=409, detail=f"El libro con ISBN {book_data.isbn} ya existe.")

            book_to_save = Book(**book_data.dict())

            save_book_to_db(book_to_save)
            return api_response(data=book_data.dict(), detail="Libro creado exitosamente", status_code=201)
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise e

    async def get_book_by_id(self, id: int):
        try:
            existing_book = find_book_by_id_to_db(id)
            if not existing_book:
                raise HTTPException(status_code=404, detail=f"El libro con ID {id} no existe.")
            return api_response(data=existing_book.dict(), detail="Libro encontrado exitosamente")
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")

    async def update_book_by_id(self, id: int, book: BookUpdate):
        try:
            # Usamos exclude_unset para enviar solo los campos que el usuario quiere actualizar.
            update_data = book.dict(exclude_unset=True)
            if not update_data:
                raise HTTPException(status_code=400, detail="No se proporcionaron datos para actualizar.")

            updated_book = update_book_to_db(id, update_data)
            if not updated_book:
                raise HTTPException(status_code=404, detail=f"El libro con ID {id} no existe.")
            return api_response(data=book.dict(), detail="Libro actualizado exitosamente", status_code=200)
        except HTTPException as http_exc:
            raise http_exc
        except ValueError as ve:
            raise HTTPException(status_code=409, detail=str(ve))
        except Exception as e:
            raise e
"""
    async def delete_book_by_id(self, id: int):
        pass

# --------------------------------------------------------------------
#  >> Servicios para Endpoints con Integración Externa (Importante)

    async def calculate_book_price(self):
        pass

# --------------------------------------------------------------------
#  >> Servicios para Endpoints Opcionales

    async def search_books(self):
        pass

    async def low_stock_books(self):
        pass
"""