import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="REVIVEPAY", page_icon="🤖")
st.title("REVIVEPAY")
st.caption("Agentic Conversational Checkout & Payment Recovery")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_product" not in st.session_state:
    st.session_state.current_product = None

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("What would you like to buy?")
if prompt:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Call backend chat API
    res = requests.post(f"{API_URL}/chat", json={"message": prompt})
    data = res.json()["response"]
    
    if data["type"] == "product_found":
        product = data["product"]
        st.session_state.current_product = product
        reply = data["message"]
    else:
        reply = data["message"]
        st.session_state.current_product = None
    
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# Product card with Pay button
if st.session_state.current_product:
    product = st.session_state.current_product
    
    st.divider()
    st.subheader(f"🛒 {product['name']}")
    st.write(f"**Price:** ₹{product['price']}")
    st.write(product['description'])
    
    # Get the original user query from chat history
    user_query = ""
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            user_query = msg["content"]
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Confirm & Pay", type="primary"):
            # Step 1: Get confirmation
            res = requests.post(f"{API_URL}/pay", json={
                "product_id": product["id"],
                "confirm": False,
                "customer_query": user_query
            })
            
            # Step 2: Actually pay
            res2 = requests.post(f"{API_URL}/pay", json={
                "product_id": product["id"],
                "confirm": True,
                "customer_query": user_query
            })
            data2 = res2.json()
            
            if data2["status"] == "success":
                st.success("Payment link generated!")
                st.link_button("💳 Pay Now", data2["payment_link"])
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Click here to complete payment: {data2['payment_link']}"
                })
            else:
                st.error("Payment Failed")
                st.info(data2["message"])
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": data2["message"]
                })
            
            st.session_state.current_product = None
            st.rerun()
    
    with col2:
        if st.button("❌ Cancel"):
            st.session_state.current_product = None
            st.rerun()

# Sidebar: Audit Dashboard
with st.sidebar:
    st.header("📊 Audit Log")
    st.write("All transactions recorded")
    
    try:
        res = requests.get(f"{API_URL}/transactions")
        txns = res.json()
        
        for txn in txns:
            status_color = "🟢" if txn["status"] == "success" else "🔴" if txn["status"] == "failed" else "🟡"
            with st.expander(f"{status_color} #{txn['id']} - {txn['product_name']}"):
                st.write(f"**Query:** {txn.get('customer_query', 'N/A')}")
                st.write(f"**Amount:** ₹{txn['amount']}")
                st.write(f"**Status:** {txn['status']}")
                if txn.get("failure_reason"):
                    st.write(f"**Failure:** {txn['failure_reason']}")
                if txn.get("recovery_action"):
                    st.write(f"**Recovery:** {txn['recovery_action']}")
                if txn.get("razorpay_link"):
                    st.write(f"**Link:** {txn['razorpay_link']}")
    except Exception as e:
        st.warning("Start the backend server to see transactions")
