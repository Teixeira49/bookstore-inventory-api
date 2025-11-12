from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=True)
    isbn = Column(String, nullable=False)
    cost_usd = Column(Float, nullable=False)
    selling_price_local = Column(String, default=None, nullable=True)
    stock_quantity = Column(Integer, nullable=False)
    category = Column(String, nullable=True)
    supplier_country = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Book title={self.title}, id={self.id}>"
    
    def get_isbn(self):
        return self.isbn
    
    def get_title(self):
        return self.title
    
    def get_author(self):
        return self.author
    
    def get_cost_usd(self):
        return self.cost_usd
    
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "cost_usd": self.cost_usd,
            "selling_price_local": self.selling_price_local,
            "stock_quantity": self.stock_quantity,
            "category": self.category,
            "supplier_country": self.supplier_country,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }