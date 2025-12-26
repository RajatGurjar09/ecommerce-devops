from database import engine, Base
from models import Order, OrderItem

# Create tables
Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")

