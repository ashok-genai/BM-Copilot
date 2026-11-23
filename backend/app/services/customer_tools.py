
from sqlalchemy.orm import Session

from app.models.customer import Customer


def list_customers(db: Session):

    customers = (
        db.query(Customer)
        .order_by(Customer.id)
        .all()
    )

    return [
        {
            "customer_code": customer.customer_code,
            "customer_name": customer.customer_name,
            "company_name": customer.company_name,
            "email": customer.email,
            "phone": customer.phone,
            "is_active": customer.is_active
        }
        for customer in customers
    ]


def count_customers(db: Session):

    total_customers = db.query(Customer).count()

    return {
        "total_customers": total_customers
    }


def find_customer_by_code(db: Session, customer_code: str):

    customer = (
        db.query(Customer)
        .filter(Customer.customer_code == customer_code)
        .first()
    )

    if customer is None:
        return {"message": "Customer not found"}

    return {
        "customer_code": customer.customer_code,
        "customer_name": customer.customer_name,
        "company_name": customer.company_name,
        "email": customer.email,
        "phone": customer.phone,
        "is_active": customer.is_active
    }
