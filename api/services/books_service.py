from typing import Optional
from fastapi import HTTPException

from api.services.database_service import *
from api.services.exchanges_service import *
from api.schemas.book_schema import BookCreate, BookUpdate, LocalCurrency
from api.models.book import Book
from api.utils.response_wrapper import api_response
from api.utils.constants import Constants


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
        

# --------------------------------------------------------------------
#  >> Servicios para Endpoints con Integración Externa (Importante)
    async def calculate_book_price(self, id: int, currency_code: LocalCurrency):
        try:
            existing_book = find_book_by_id_to_db(id)
            if not existing_book:
                raise HTTPException(status_code=404, detail=f"El libro con ID {id} no existe.")
            
            exchanges = get_global_exchanges()

            if currency_code.code not in exchanges["data"].keys():
                raise HTTPException(status_code=404, detail=f"El codigo de moneda {currency_code.code} no esta disponible")

            exchange_rate = exchanges["data"][currency_code.code]

            new_local_price = self.calculate_local_price(existing_book.get_cost_usd(), exchange_rate)
            new_selling_price_local = self.calculate_profit(new_local_price)

            update_selling_price_local(existing_book, new_selling_price_local)

            response_data = {
                "book_id": existing_book.id,
                "cost_usd": existing_book.cost_usd,
                "exchange_rate": exchange_rate,
                "cost_local": new_local_price,
                "margin_percentage": Constants.PROFIT_MARGIN * 100,
                "selling_price_local": new_selling_price_local,
                "currency": currency_code.code,
                "calculation_timestamp": datetime.now()
            }

            return api_response(data=response_data, detail="Precio actualizado exitosamente", status_code=200)
        except HTTPException as http_exc:
            raise http_exc
        except ValueError as ve:
            raise HTTPException(status_code=409, detail=str(ve))
        except Exception as e:
            raise e
        
    async def delete_book_by_id(self, id: int):
        try:
            deleted_book = delete_book_by_id_to_db(id)
            if not deleted_book:
                raise HTTPException(status_code=404, detail=f"El libro con ID {id} no existe y no pudo ser eliminado.")
            
            return api_response(data={"deleted_book_id": id}, detail="Libro eliminado exitosamente", status_code=200)
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")

    def calculate_profit(self, local_price: float):
        return local_price + (local_price * Constants.PROFIT_MARGIN)

    def calculate_local_price(self, cost_usd: float, exchange_rate: float):
        return cost_usd * exchange_rate
"""
# --------------------------------------------------------------------
#  >> Servicios para Endpoints Opcionales

    async def search_books(self):
        pass

    async def low_stock_books(self):
        pass
"""