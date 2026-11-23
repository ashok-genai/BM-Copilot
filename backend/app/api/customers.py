
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerResponse

router = APIRouter()


@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):

    try:
        # Convert API data into a database object
        new_customer = Customer(**customer_data.model_dump())

        # Add customer to database
        db.add(new_customer)

        # Save changes
        db.commit()

        # Refresh to get database-generated values
        db.refresh(new_customer)

        return new_customer

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Customer code or email already exists"
        )

# Get all customers
@router.get("/", response_model=list[CustomerResponse])
def get_all_customers(db: Session = Depends(get_db)):

    customers = db.query(Customer).order_by(Customer.id).all()

    return customers


# Get customer by ID
@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer_by_id(
    customer_id: int,
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


# Update customer
@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    try:
        # Update customer details
        update_data = customer_data.model_dump()

        for key, value in update_data.items():
            setattr(customer, key, value)

        # Save changes
        db.commit()

        # Refresh updated customer
        db.refresh(customer)

        return customer

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Customer code or email already exists"
        )


# Delete customer
@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):

    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    db.delete(customer)
    db.commit()

    return {
        "message": "Customer deleted successfully",
        "customer_id": customer_id
    }
