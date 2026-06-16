from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Table, Float, Column, DateTime, func

from datetime import datetime

from database import Base


    
#Junction Table/ Association Table
dish_category = Table(
                    "dish_category",
                    Base.metadata,
                    Column("dish_id", Integer, ForeignKey("dishes.id"), primary_key=True),
                    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True)
                    )


    
#SQLALchemy models   
#Category Table 
class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    dishes = relationship("Dish", secondary=dish_category, back_populates="categories")
 
#Dish Table   
class Dish(Base):
    __tablename__ = "dishes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(String(1000))
    price: Mapped[float] = mapped_column(Float)
    
    categories = relationship("Category", secondary=dish_category, back_populates="dishes")
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="dish")
    
    
    
#Order Table
class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("customers.id"))
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
  
    customer: Mapped["Customer"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order")
   
#Customer Table 
class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20), unique=True)  
    
    orders: Mapped[list["Order"]] = relationship(back_populates="customer")
    
#Junction Association Table OrderItem  
class OrderItem(Base):
    __tablename__ = "order_items"
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"), primary_key=True)
    dish_id: Mapped[int] = mapped_column(Integer, ForeignKey("dishes.id"), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
    
    order: Mapped["Order"] = relationship(back_populates="items")
    dish: Mapped["Dish"] = relationship(back_populates="order_items")
    
        

