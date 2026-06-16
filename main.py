from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select   

from schemes import DishCreate, CategoryCreate, CustomerCreate, PlaceOrder, CustomerResponse, DishResponse, CategoryResponse, OrderResponse
from dependencies import get_db
from models import Category, Dish, Customer, Order, OrderItem


app = FastAPI()

#Home Page
@app.get("/")
def index():
    return {"message": "Welcome! Taste the Tide at Snaji’s "}

#Admin response
@app.post("/dishes/")
def create_dish(dish: DishCreate, db: Session = Depends(get_db)):
    
    categories = db.query(Category).filter(Category.id.in_(dish.categories)).all()
    
    if len(categories) != len(dish.categories):
        raise HTTPException(status_code=400, detail="Some Category IDs is not found")
    
    new_dish = Dish(name=dish.name, description=dish.description, price=dish.price, categories=categories)
    
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    
    return {
    "id": new_dish.id,
    "name": new_dish.name,
    "price": new_dish.price,
    "categories": [{"id": c.id, "name": c.name} for c in new_dish.categories]
    }
 
#Customer Request
@app.get("/dishes/{dish_name}")
def get_dish(dish_name: str, db: Session=Depends(get_db)):
    stmt = select(Dish).where(Dish.name == dish_name)
    result = db.execute(stmt)
    dish = result.scalar_one_or_none()
    if dish is None:
        raise HTTPException(status_code=404, detail=f"{dish_name} is Not Available!")
    return dish

#Admin Response
@app.post("/categories/")
def create_category(category: CategoryCreate, db: Session=Depends(get_db)):
    
    new_category = Category(name=category.name)
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return {
        "id": new_category.id,
        "name": new_category.name
    }
    
#Customer request    
@app.get("/categories/{category}")
def get_category(category: str, db: Session = Depends(get_db)):
    stmt = select(Category).where(Category.name==category)
    result = db.execute(stmt)
    cat = result.scalar_one_or_none()
    
    if cat is None:
        raise HTTPException(status_code=404, detail=f"{category} Not Found!")
    return cat


#Customer register
@app.post("/customers/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
        
    new_customer = Customer(name=customer.name, phone=customer.phone)
    
    stmt = select(Customer).where(Customer.phone == new_customer.phone)
    result = db.execute(stmt)
    existing_customer = result.scalar_one_or_none()
    
    #To validate wheather the user already have account
    if existing_customer:
        raise HTTPException(status_code=400, detail="Phone number already exists") #To avoid internal server error
    
    #If not then insert into database
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    
    return {
        "id": new_customer.id,
        "name": new_customer.name,
        "phone": new_customer.phone
    }

#Admin Fetch customer details
@app.get("/customers/{id}", response_model=CustomerResponse)
def get_customer(id: int, db : Session = Depends(get_db)):
    
    customer = db.execute(
        select(Customer).where(Customer.id == id)
    ).scalar_one_or_none()
    
    if customer is None:
        raise HTTPException(status_code=404, detail="User Not Found!")
    
    return customer

#Customers to place orders
@app.post("/orders/", response_model=OrderResponse)
def place_orders(order: PlaceOrder, db: Session = Depends(get_db)):
    
    dish = db.execute(
        select(Dish).where(Dish.name==order.dish)
    ).scalar_one_or_none()
    
    if dish is None:
        raise HTTPException(status_code=404, detail="Dish Not Available!")
    
    customer = db.execute(
        select(Customer).where(Customer.id == order.customer_id)
    ).scalar_one_or_none()
    
    if customer is None:
        raise HTTPException(status_code=404, detail= "Customer Not Found")
    
    new_order = Order(customer_id=customer.id, status="pending")

    db.add(new_order)
    db.commit()
    db.refresh(new_order)    
    
    
    new_item = OrderItem(
        order_id = new_order.id,
        dish_id = dish.id,
        quantity = order.quantity,
        unit_price = dish.price
    )
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    return {
    "order_id": new_order.id,
    "customer_id": customer.id,
    "dish": dish.name,
    "quantity": new_item.quantity,
    "status": new_order.status
    }