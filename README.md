# REVIVEPAY

**Agentic Conversational Checkout & Intelligent Payment Recovery System**

Built for Razorpay AI Buildathon 2026 — Track 01: AI Growth & Agentic Commerce.

---

## 🎥 Demo

[Link to your 5-min pitch video will go here]

---

## 🚀 What It Does

REVIVEPAY is an AI-powered conversational checkout agent for small merchants. Customers discover and purchase products simply by chatting, while the system intelligently recovers failed payments instead of letting them drop.

### Core Features

| Feature | Description |
|---------|-------------|
| **Conversational Checkout** | Chat with an AI agent to find and buy products across an 8-item catalog |
| **Razorpay Integration** | Generates real payment links via Razorpay Test API |
| **Safety Guardrails** | Double-confirmation before any payment link is generated — no money moves without explicit human confirmation |
| **Intelligent Recovery** | Diagnoses payment failures and suggests retry, switch method, or save for later |
| **Post-Payment Upsell** | Suggests relevant add-ons after a successful purchase |
| **Audit Dashboard** | Full transaction log with status, failure reasons, and recovery actions |
| **Recovery Analytics** | Live metrics — total revenue, success rate, recovery rate |

---

## 🏗️ Architecture

```
Customer Chat
    ↓
[AI Agent] → Product Search (SQLite)
    ↓
[Payment Engine] → Razorpay Payment Link (with confirmation guardrail)
    ↓
[Success] → Upsell / Complete
[Failure] → [Recovery Engine] → Smart retry / switch / save
    ↓
[Audit Log] → SQLite Transactions Table
```

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy, SQLite
- **AI Agent:** Keyword-matching search + structured validation
- **Payments:** Razorpay Payment Links API (Test Mode)
- **Frontend:** Streamlit
- **Deployment:** Local (Render/Streamlit Cloud planned)

---

## ⚡ Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/Palak6512/Revivepay.git
cd Revivepay
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Add API Keys
Create a `.env` file:
```
RAZORPAY_KEY_ID=your_test_key
RAZORPAY_KEY_SECRET=your_test_secret
```

### 3. Run Backend
```bash
DEMO_MODE=true uvicorn main:app --reload
```

### 4. Run Frontend (new terminal)
```bash
streamlit run app.py
```

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | AI agent chat — finds products from natural language |
| `/products` | GET | Full product catalog |
| `/pay` | POST | Initiate payment with confirmation guardrail |
| `/transactions` | GET | Audit log of every transaction |
| `/upsell/{product_id}` | GET | Recommended add-on for a purchased product |

---

## 🧠 Build Challenges & How I Solved Them

**Challenge 1: Reliable demo without depending on live payment gateway behavior**
Razorpay's test API can fail unpredictably, which made consistent demos hard. Added a `DEMO_MODE` environment flag that simulates guaranteed successful payments for demonstration purposes, while the real Razorpay integration remains fully functional and testable.

**Challenge 2: Search matching wrong products**
Simple keyword matching returned the wrong item when colors or attributes didn't match (e.g., "white sneakers" matching "Blue Sneakers"). Rebuilt the matcher with exact-match, word-match, and category-match tiers, falling back to a friendly catalog listing when nothing matches.

**Challenge 3: Payment failure recovery logic**
Needed to differentiate between retryable failures (timeout) vs non-retryable (insufficient funds). Built a rule-based recovery engine that maps error patterns to specific recovery actions and logs the reasoning in the audit trail.

**Challenge 4: Invalid payload handling**
Tested and confirmed the API gracefully rejects invalid requests (e.g., a nonexistent `product_id`) with a clean 404 response instead of crashing — verified via direct API calls.

---
## 🔮 Limitations & Future Work

- **Rule-based, not LLM-based:** Product search, upsell recommendations, and failure recovery currently use deterministic keyword-matching and rule-based logic rather than LLM calls. This was a deliberate choice — for a small, fixed catalog, rules are faster, cheaper, and fully explainable with zero hallucination risk. A future version could use an LLM for more open-ended queries or ambiguous failure diagnosis where rules alone aren't sufficient.
- **Upsell mapping is static:** Currently a fixed lookup by product ID. A future version would personalize suggestions using purchase history or embeddings.
- **Recovery Response Rate measures guidance coverage, not confirmed recovery:** It currently tracks the percentage of failed transactions that received a recovery message, not whether the customer ultimately completed the payment. A future version would track actual retry-to-success conversion.

---

## 👤 Author

**Palak Tyagi** — 3rd Year BTech AI, aspiring AI/ML Engineer with a focus on Agentic AI & AI Product Management.
