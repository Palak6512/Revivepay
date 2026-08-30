import streamlit as st
import requests
import time

API_URL = "http://localhost:8000"

# Page config
st.set_page_config(page_title="REVIVEPAY", page_icon="🤖", layout="wide")

# Custom CSS for visual effects
st.markdown("""
<style>
    .main-title {
        font-size: 3rem !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .upsell-box {
        padding: 1rem;
        border-radius: 15px;
        border: 2px solid #f39c12;
        background: linear-gradient(135deg, #f5af19 0%, #f12711 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(243, 156, 18, 0.4);
    }
    .metric-card {
        background: #1e1e1e;
        padding: 10px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
    .stButton>button {
        border-radius: 20px !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-title">REVIVEPAY</h1>', unsafe_allow_html=True)
st.caption("Agentic Conversational Checkout & Intelligent Payment Recovery")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    st.toggle(
        "🎬 Demo Mode (Guaranteed Success)",
        value=True,
        help="Backend controls this via the DEMO_MODE env var. Turn it on there before your demo so payments always succeed and judges can see the upsell flow."
    )

    try:
        status = requests.get(f"{API_URL}/demo-status").json()
        if status.get("demo_mode"):
            st.success("🎬 Demo Mode: ON (backend)")
        else:
            st.info("🔴 Real Mode: using actual Razorpay API")
    except Exception:
        st.warning("Backend not running")

    st.divider()

    tab1, tab2 = st.tabs(["📊 Analytics", "📋 Audit Log"])

    with tab1:
        st.header("Recovery Analytics")
        try:
            res = requests.get(f"{API_URL}/transactions")
            txns = res.json()
            total = len(txns)
            successful = sum(1 for t in txns if t["status"] == "success")
            failed = sum(1 for t in txns if t["status"] == "failed")
            recovered = sum(1 for t in txns if t.get("recovery_action"))
            total_revenue = sum(t["amount"] for t in txns if t["status"] == "success")

            c1, c2 = st.columns(2)
            with c1:
                st.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
            with c2:
                st.metric("📦 Total Orders", total)

            c3, c4 = st.columns(2)
            with c3:
                st.metric("✅ Successful", successful)
            with c4:
                st.metric("❌ Failed", failed)

            if total > 0:
                success_rate = (successful / total) * 100
                st.progress(success_rate / 100, text=f"Success Rate: {success_rate:.1f}%")
            if failed > 0:
                recovery_rate = (recovered / failed) * 100
                st.progress(recovery_rate / 100, text=f"Recovery Response Rate: {recovery_rate:.1f}%")

        except Exception:
            st.warning("Start backend to see analytics")

    with tab2:
        st.header("Transaction Audit")
        try:
            res = requests.get(f"{API_URL}/transactions")
            txns = res.json()
            for txn in reversed(txns):
                if txn["status"] == "success":
                    emoji, color = "✅", "green"
                elif txn["status"] == "failed":
                    emoji, color = "❌", "red"
                else:
                    emoji, color = "⏳", "orange"

                with st.expander(f"{emoji} #{txn['id']} — {txn['product_name']} (₹{txn['amount']})"):
                    st.write(f"**Query:** {txn.get('customer_query', 'N/A')}")
                    st.write(f"**Status:** :{color}[{txn['status']}]")
                    if txn.get("failure_reason"):
                        st.write(f"**Reason:** {txn['failure_reason']}")
                    if txn.get("recovery_action"):
                        st.write(f"**Recovery:** {txn['recovery_action']}")
                    if txn.get("razorpay_link"):
                        st.write(f"**Link:** `{txn['razorpay_link']}`")
        except Exception:
            st.warning("Start backend to see audit log")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_product" not in st.session_state:
    st.session_state.current_product = None
if "show_upsell" not in st.session_state:
    st.session_state.show_upsell = None
if "show_confetti" not in st.session_state:
    st.session_state.show_confetti = False

if st.session_state.show_confetti:
    st.balloons()
    st.session_state.show_confetti = False
    time.sleep(0.5)

# ---------------- CHAT ----------------
st.divider()
st.subheader("💬 Chat with your Shopping Assistant")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("What would you like to buy? (Try: blue sneakers, backpack, smart watch...)")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    res = requests.post(f"{API_URL}/chat", json={"message": prompt})
    data = res.json()["response"]

    if data["type"] == "product_found":
        product = data["product"]
        st.session_state.current_product = product
        st.session_state.show_upsell = None
        reply = data["message"]
    else:
        reply = data["message"]
        st.session_state.current_product = None
        st.session_state.show_upsell = None

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# ---------------- PRODUCT CARD ----------------
if st.session_state.current_product:
    product = st.session_state.current_product
    st.divider()

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader(f"🛒 {product['name']}")
        st.write(f"**Category:** {product.get('category', 'General')}")
        st.write(f"**Price:** :green[₹{product['price']}]")
        st.info(product['description'])

    with col2:
        user_query = ""
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                user_query = msg["content"]

        if st.button("✅ Confirm & Pay", type="primary", use_container_width=True):
            with st.spinner("Processing payment..."):
                requests.post(f"{API_URL}/pay", json={
                    "product_id": product["id"],
                    "confirm": False,
                    "customer_query": user_query
                })
                res2 = requests.post(f"{API_URL}/pay", json={
                    "product_id": product["id"],
                    "confirm": True,
                    "customer_query": user_query
                })
                data2 = res2.json()

            if data2["status"] == "success":
                st.session_state.show_confetti = True
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"✅ {product['name']} confirmed! Complete payment here: {data2['payment_link']}"
                })

                upsell_res = requests.get(f"{API_URL}/upsell/{product['id']}")
                upsell_data = upsell_res.json()
                if upsell_data.get("has_upsell"):
                    st.session_state.show_upsell = upsell_data["product"]
                else:
                    st.session_state.show_upsell = None
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"❌ {data2['message']}"
                })
                st.session_state.show_upsell = None

            st.session_state.current_product = None
            st.rerun()

        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.current_product = None
            st.session_state.show_upsell = None
            st.rerun()

# ---------------- UPSELL ----------------
if st.session_state.show_upsell:
    upsell = st.session_state.show_upsell
    st.divider()
    st.markdown(f"""
    <div class="upsell-box">
        <h3>🎯 Recommended Add-on</h3>
        <p style="font-size:1.3rem;"><b>{upsell['name']}</b> — ₹{upsell['price']}</p>
        <p>{upsell['reason']}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button(f"Add {upsell['name']} to Order", type="secondary"):
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"🛍️ Great choice! {upsell['name']} (₹{upsell['price']}) added to your wishlist."
        })
        st.session_state.show_upsell = None
        st.rerun()
