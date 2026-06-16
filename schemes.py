from pydantic import BaseModel, Field, ConfigDict


#Pydantic scheme for Validation
class DishCreate(BaseModel):
    name: str
    description: str | None = None
    price: float = Field(gt=0)
    categories: list[int]


class DishResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class PlaceOrder(BaseModel):
    customer_id: int
    dish: str
    quantity: int = Field(gt=0)


class OrderResponse(BaseModel):
    order_id: int
    customer_id: int
    dish: str
    quantity: int
    status: str


class CustomerCreate(BaseModel):
    name: str
    phone: str


class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str

    model_config = ConfigDict(from_attributes=True)