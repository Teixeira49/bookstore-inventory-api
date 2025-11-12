from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from typing import Optional

from ..models.book import Base, Book

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("No DATABASE_URL environment variable set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Crear tablas si no existen."""
    Base.metadata.create_all(bind=engine)

def get_books_to_db():
    init_db()
    session = SessionLocal()
    try:
        books = session.query(Book).order_by(Book.id).all()
        return books
    except Exception:
        raise
    finally:
        session.close()

def get_books_paginated_to_db(page: int = 0, limit: int = 10):
    init_db()
    session = SessionLocal()
    try:
        skip = page * limit
        books = session.query(Book).order_by(Book.id).offset(skip).limit(limit).all()
        total_items = session.query(Book).count()
        return books, total_items
    except Exception:
        raise
    finally:
        session.close()


def find_book_by_isbn_to_db(isbn: str):
    init_db()
    session = SessionLocal()
    try:
        book = session.query(Book).filter(Book.isbn == isbn).first()
        return book
    except Exception:
        raise
    finally:
        session.close()

def find_book_by_id_to_db(id: int):
    init_db()
    session = SessionLocal()
    try:
        book = session.query(Book).filter(Book.id == id).first()
        return book
    except Exception:
        raise
    finally:
        session.close()


def save_book_to_db(book_data: Book):
    init_db()
    session = SessionLocal()
    try:
        existing_book = session.query(Book).filter(Book.isbn == book_data.isbn).first()

        if existing_book:
            raise
        else:
            session.add(book_data)

        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def update_book_to_db(id: int, book_data: dict):
    init_db()
    session = SessionLocal()
    try:
        existing_book = session.query(Book).filter(Book.id == id).first()
        if not existing_book:
            return None

        new_isbn = book_data.get("isbn")
        new_title = book_data.get("title")
        
        check_coincidences = session.query(Book).filter(Book.id != id).filter((Book.isbn == new_isbn) | (Book.title == new_title)).first()
        if check_coincidences:
            raise ValueError(f"Ya existe otro libro con el mismo ISBN ('{new_isbn}') o título ('{new_title}').")
        
        update_book(existing_book, book_data)
        
        session.commit()
        return existing_book
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def update_book(existing_book: Book, book_data: dict):
    for key, value in book_data.items():
        if value is not None:
            setattr(existing_book, key, value)
    return existing_book

def delete_book_by_id_to_db(id: int):
    init_db()
    session = SessionLocal()
    try:
        book_to_delete = session.query(Book).filter(Book.id == id).first()
        if not book_to_delete:
            return None
        
        session.delete(book_to_delete)
        session.commit()
        return book_to_delete
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def update_selling_price_local(book_data: Book, new_price: float):
    init_db()
    session = SessionLocal()
    try:
        existing_book = session.query(Book).filter(Book.isbn == book_data.isbn).first()
        if not existing_book:
            raise
        
        existing_book.selling_price_local = new_price
        session.commit()
        return existing_book
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def search_category_to_db(category: Optional[str]):
    init_db()
    session = SessionLocal()
    try:
        query = session.query(Book)
        if category:
            query = query.filter(Book.category.ilike(f"%{category}%"))
        books = query.order_by(Book.category, Book.id).all()
        return books
    except Exception:
        raise
    finally:
        session.close()

def search_by_stock_quantity_to_db(threshold: Optional[int]):
    init_db()
    session = SessionLocal()
    try:
        query = session.query(Book)
        if threshold is not None:
            query = query.filter(Book.stock_quantity <= threshold)
        books = query.order_by(Book.stock_quantity, Book.id).all()
        return books
    except Exception:
        raise
    finally:
        session.close()

def search_category_paginated_to_db(
        category: Optional[str],
        page: Optional[int] = None,
        limit: Optional[int] = None
    ):
    init_db()
    session = SessionLocal()
    try:
        query = session.query(Book)
        if category:
            skip = page * limit
            query = query.filter(Book.category.ilike(f"%{category}%"))
            books = query.order_by(Book.category, Book.id).offset(skip).limit(limit).all()
            total_items = query.count()
            return books, total_items
        books = query.order_by(Book.category, Book.id).all()
        total_items = query.count()
        return books, total_items
    except Exception:
        raise
    finally:
        session.close()

def search_by_stock_quantity_paginated_to_db(
    threshold: Optional[int],
    page: Optional[int] = None,
    limit: Optional[int] = None
):
    init_db()
    session = SessionLocal()
    try:
        query = session.query(Book)
        if threshold is not None:
            skip = page * limit
            query = query.filter(Book.stock_quantity <= threshold)
            books = query.order_by(Book.stock_quantity, Book.id).offset(skip).limit(limit).all()
            total_items = query.count()
            return books, total_items
        books = query.order_by(Book.stock_quantity, Book.id).all()
        total_items = query.count()
        return books, total_items
    except Exception:
        raise
    finally:
        session.close()