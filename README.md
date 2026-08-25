# REVIVEPAY

**Agentic Conversational Checkout & Intelligent Payment Recovery System**

Built for Razorpay AI Buildathon 2026 — Track 01: AI Growth & Agentic Commerce.

---

## 🎥 Demo

[Link to your 5-min pitch video will go here]

---

## 🚀 What It Does

REVIVEPAY is an AI-powered conversational checkout agent for small merchants. Customers can discover and purchase products simply by chatting, while the system intelligently recovers failed payments instead of letting them drop.

### Core Features

| Feature | Description |
|---------|-------------|
| **Conversational Checkout** | Chat with an AI agent to find and buy products |
| **Razorpay Integration** | Generates real payment links via Razorpay Test API |
| **Safety Guardrails** | Double-confirmation before any payment link is generated |
| **Intelligent Recovery** | Diagnoses payment failures and suggests retry, switch method, or save for later |
| **Audit Dashboard** | Full transaction log with status, failure reasons, and recovery actions |

---

## 🏗️ Architecture
# REVIVEPAY

Agentic Conversational Checkout & Intelligent Payment Recovery System

Built for Razorpay AI Buildathon 2026 — Track 01: AI Growth & Agentic Commerce.

## What It Does

REVIVEPAY lets customers buy products by chatting with an AI agent. When payment fails, it intelligently recovers the transaction instead of dropping it.

- Conversational product search
- Razorpay Payment Links integration (Test Mode)
- Double-confirmation safety guardrail
- Smart payment failure recovery (retry / switch method / save for later)
- Full audit dashboard

## Tech Stack

Python | FastAPI | SQLite | OpenAI | Razorpay API | Streamlit

## Quick Start

```bash
git clone https://github.com/Palak6512/Revivepay.git
cd Revivepay
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
