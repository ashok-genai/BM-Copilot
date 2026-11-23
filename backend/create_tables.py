
from app.core.database import Base, engine
from app.models.customer import Customer

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")
