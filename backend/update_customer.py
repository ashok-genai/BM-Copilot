
from app.core.database import SessionLocal
from app.models.customer import Customer

# Create database session
db = SessionLocal()

try:
    # Find the customer
    customer = db.query(Customer).filter_by(
        customer_code="CUST001"
    ).first()

    if customer:
        # Update phone number
        customer.phone = "9000011111"

        # Save changes
        db.commit()

        print("Customer updated successfully!")

    else:
        print("Customer not found!")

except Exception as error:
    db.rollback()
    print("Error:", error)

finally:
    db.close()
