import razorpay
import os
from dotenv import load_dotenv

load_dotenv()

client = razorpay.Client(auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET")))

def create_payment_link(product_name: str, amount_paise: int, transaction_id: int):
    """
    Create a Razorpay payment link in TEST mode.
    amount_paise: amount in paise (₹1499 = 149900 paise)
    """
    try:
        payment_link = client.payment_link.create({
            "amount": amount_paise,
            "currency": "INR",
            "description": f"Payment for {product_name} (Order #{transaction_id})",
            "callback_url": "http://localhost:8000/callback",
            "callback_method": "get"
        })
        return payment_link["short_url"]
    except Exception as e:
        raise Exception(f"Razorpay error: {str(e)}")

def simulate_payment_failure():
    """For demo purposes - simulate a Razorpay failure"""
    raise Exception("Gateway timeout - bank not responding")
