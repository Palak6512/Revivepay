from database import Transaction

def handle_payment_failure(txn: Transaction, db):
    """
    Intelligent recovery engine.
    Analyzes failure and suggests recovery action.
    """
    failure = txn.failure_reason or "Unknown error"
    failure_lower = failure.lower()
    
    # Recovery logic based on failure type
    if "timeout" in failure_lower or "network" in failure_lower:
        txn.recovery_action = "retry"
        db.commit()
        return "It looks like a network timeout. You can retry the payment now."
    
    elif "card" in failure_lower or "declined" in failure_lower:
        txn.recovery_action = "switch_method"
        db.commit()
        return "Your card was declined. Try UPI or a different card."
    
    elif "insufficient" in failure_lower:
        txn.recovery_action = "save_for_later"
        db.commit()
        return "Insufficient funds. I've saved this item for you. Complete the purchase later."
    
    else:
        txn.recovery_action = "retry"
        db.commit()
        return "Payment failed. Please retry or try a different payment method."

def simulate_failure_scenario(scenario: str):
    """For testing - simulate different failure types"""
    scenarios = {
        "timeout": "Gateway timeout - bank not responding",
        "declined": "Card declined by issuing bank",
        "insufficient": "Insufficient funds in account",
        "risk": "Transaction blocked by risk system"
    }
    return scenarios.get(scenario, "Unknown payment failure")
