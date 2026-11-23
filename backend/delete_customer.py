
from app.core.database import SessionLocal
from app.models.customer import Customer

# Create database session
db = SessionLocal()

try:
    # Find the customer
    customer = db.query(Customer).filter_by(
        customer_code="CUST002"
    ).first()

    if customer:
        # Delete the customer
        db.delete(customer)

        # Save changes
        db.commit()

        print("Customer deleted successfully!")

    else:
        print("Customer not found!")

except Exception as error:
    db.rollback()
    print("Error:", error)

finally:
    db.close()
