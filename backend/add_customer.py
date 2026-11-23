
from app.core.database import SessionLocal
from app.models.customer import Customer

# Create database session
db = SessionLocal()

try:
    # Check whether customer already exists
    existing_customer = db.query(Customer).filter_by(
        customer_code="CUST001"
    ).first()

    if existing_customer:
        print("Customer already exists!")

    else:
        # Create a new customer
        new_customer = Customer(
            customer_code="CUST001",
            customer_name="ABC Industries",
            email="abc@example.com",
            phone="9876543210",
            company_name="ABC Industries Pvt Ltd",
            address="Chennai, Tamil Nadu"
        )

        # Add customer to database
        db.add(new_customer)

        # Save changes
        db.commit()

        print("Customer added successfully!")

except Exception as error:
    db.rollback()
    print("Error:", error)

finally:
    db.close()
