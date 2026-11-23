
from pydantic import BaseModel, ConfigDict
from datetime import datetime


# Data required to create a customer
class CustomerCreate(BaseModel):
    customer_code: str
    customer_name: str
    email: str | None = None
    phone: str | None = None
    company_name: str | None = None
    address: str | None = None
    is_active: bool = True


# Data returned by the API
class CustomerResponse(BaseModel):
    id: int
    customer_code: str
    customer_name: str
    email: str | None = None
    phone: str | None = None
    company_name: str | None = None
    address: str | None = None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
