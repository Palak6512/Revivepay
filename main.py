from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, Product, Transaction
from models import ChatMessage, PaymentRequest, PaymentResponse, TransactionLog
from agent import find_product, generate_chat_response
from recovery import handle_payment_failure
from razorpay_client import create_payment_link
import json

app = FastAPI(title="REVIVEPAY")

@app.on_event("startup")
def load_products():
    db = next(get_db())
    if db.query(Product).count() == 0:
        with open("products.json", "r") as f2:
            products = json.load(f2)
            for p in products:
                db.add(Product(**p))
            db.commit()

@app.post("/chat")
def chat(msg: ChatMessage, db: Session = Depends(get_db)):
    response = generate_chat_response(msg.message, db)
    return {"response": response}

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.post("/pay", response_model=PaymentResponse)
def initiate_payment(req: PaymentRequest, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == req.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    txn = Transaction(
        product_id=product.id,
        product_name=product.name,
        amount=product.price,
        status="pending",
        customer_query=req.customer_query
    )
    db.add(txn)
    db.commit()
    db.refresh(txn)
    
    if not req.confirm:
        return PaymentResponse(
            status="awaiting_confirmation",
            message=f"Please confirm: {product.name} - Rs{product.price}. Set confirm=true to proceed.",
            transaction_id=txn.id
        )
    
    try:
        link = create_payment_link(product.name, int(product.price * 100), txn.id)
        txn.razorpay_link = link
        txn.status = "success"
        db.commit()
        return PaymentResponse(
            status="success",
            message=f"Payment link generated: {link}",
            payment_link=link,
            transaction_id=txn.id
        )
    except Exception as e:
        txn.status = "failed"
        txn.failure_reason = str(e)
        db.commit()
        recovery = handle_payment_failure(txn, db)
        return PaymentResponse(
            status="failed",
            message=recovery,
            transaction_id=txn.id
        )

@app.get("/transactions", response_model=list[TransactionLog])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()
