from sqlalchemy.orm import Session
from database import Product
import json

def find_product(query: str, db: Session):
    """Simple keyword search on product name"""
    query_lower = query.lower()
    products = db.query(Product).all()
    for p in products:
        if p.name.lower() in query_lower or any(word in p.name.lower() for word in query_lower.split()):
            return p
    return None

def generate_chat_response(message: str, db: Session):
    """Generate agent response based on user message"""
    product = find_product(message, db)
    
    if product:
        return {
            "type": "product_found",
            "message": f"I found {product.name} ({product.category}) - ₹{product.price}. {product.description}. Would you like to proceed?",
            "product": {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "description": product.description
            }
        }
    
    return {
        "type": "clarification",
        "message": "I can help you find products! Try asking for sneakers, earbuds, t-shirts, smart watches, or backpacks."
    }
