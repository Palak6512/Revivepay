from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# For chat messages
class ChatMessage(BaseModel):
    message: str

# For product response
class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    price: float
    size: Optional[str] = None
    description: str

    class Config:
        from_attributes = True

# For payment request
class PaymentRequest(BaseModel):
    product_id: int
    confirm: bool = False
    customer_query: Optional[str] = None

# For payment response
class PaymentResponse(BaseModel):
    status: str
    message: str
    payment_link: Optional[str] = None
    transaction_id: Optional[int] = None

# For recovery request
class RecoveryRequest(BaseModel):
    transaction_id: int
    action: str  # retry, switch_method, save_for_later

# For audit log response
class TransactionLog(BaseModel):
    id: int
    customer_query: str
    product_name: str
    amount: float
    status: str
    failure_reason: Optional[str] = None
    recovery_action: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
