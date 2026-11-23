
from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    password_hash = Column(String, nullable=True)