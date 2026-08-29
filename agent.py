from sqlalchemy.orm import Session
from database import Product


def find_product(query: str, db: Session):
    """Smart search: exact match > partial match > category match"""
    query_lower = query.lower().strip()
    products = db.query(Product).all()
    
    # 1. Exact match (full product name in query)
    for p in products:
        if p.name.lower() in query_lower:
            return p, "exact"
    
    # 2. Word match (any word from product name matches query)
    query_words = set(query_lower.split())
    for p in products:
        product_words = set(p.name.lower().split())
        if query_words & product_words:  # intersection
            return p, "partial"
    
    # 3. Category match
    for p in products:
        if p.category.lower() in query_lower:
            return p, "category"
    
    return None, None


def generate_chat_response(message: str, db: Session):
    """Generate agent response based on user message"""
    product, match_type = find_product(message, db)
    
    if product:
        if match_type == "exact":
            msg = f"I found {product.name} ({product.category}) - ₹{product.price}. {product.description}. Would you like to proceed?"
        else:
            msg = f"I found {product.name} ({product.category}) - ₹{product.price}. {product.description}. Is this what you were looking for?"
        
        return {
            "type": "product_found",
            "message": msg,
            "product": {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "description": product.description
            }
        }
    
    # No match — show what we have (like real apps)
    all_products = db.query(Product).all()
    product_list = ", ".join([f"{p.name} (₹{p.price})" for p in all_products])
    
    return {
        "type": "clarification",
        "message": f"I don't have that exact item. Here is what is available in our store:\n\n{product_list}\n\nWhich one would you like?"
    }


def get_upsell_product(product_id: int, db):
    """Suggest a relevant add-on based on purchased product"""
    upsell_map = {
        1: {"id": 101, "name": "Premium Socks", "price": 199, "reason": "60% of sneaker buyers also get these comfortable socks"},
        2: {"id": 102, "name": "Silicone Earbud Case", "price": 299, "reason": "Protect your new earbuds from drops and dust"},
        3: {"id": 103, "name": "Baseball Cap", "price": 349, "reason": "Complete your casual look with this matching cap"},
        4: {"id": 104, "name": "Extra Watch Strap", "price": 499, "reason": "Swap styles with an additional strap for your smartwatch"},
        5: {"id": 105, "name": "Laptop Sleeve", "price": 599, "reason": "Protect your laptop alongside your new backpack"},
    }
    return upsell_map.get(product_id)
