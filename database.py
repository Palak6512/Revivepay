from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Create SQLite database
engine = create_engine('sqlite:///revivepay.db', connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# Product table
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    price = Column(Float)
    size = Column(String, nullable=True)
    description = Column(Text)

# Transaction table (for audit + recovery)
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    customer_query = Column(Text)
    product_id = Column(Integer)
    product_name = Column(String)
    amount = Column(Float)
    status = Column(String)  # pending, success, failed, recovered
    failure_reason = Column(String, nullable=True)
    recovery_action = Column(String, nullable=True)
    razorpay_link = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Helper to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
