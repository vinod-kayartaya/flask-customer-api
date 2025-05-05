from app import db
from sqlalchemy import Column, Integer, String, UniqueConstraint

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    phone = Column(String(20), unique=True)
    city = Column(String(50))
    
    def __repr__(self):
        return f'<Customer {self.name}>' 