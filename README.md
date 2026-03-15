# 🤖 Multi-Agent AI System with LLMOps
### AI-Powered ITSM Ticket Generation & Email Automation

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?style=flat-square)
![LangGraph](https://img.shields.io/badge/LangGraph-ReAct-orange?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-Llama3-purple?style=flat-square)
![SonarQube](https://img.shields.io/badge/SonarQube-Quality-red?style=flat-square)
![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-yellow?style=flat-square)

---

## 📌 Overview

A production-grade **Multi-Agent AI System** that automates IT Service Management (ITSM) ticket generation using **LangGraph ReAct Agents**, **Groq LLM (Llama 3)**, and **FastAPI**. The system reads incoming emails via Gmail, understands the user's problem in natural language (English or Urdu), generates a structured support ticket, and sends an automated reply — all without human intervention.

**LLMOps pipeline** is integrated via **Jenkins CI/CD** and **SonarQube** for code quality, ensuring the system is production-ready and maintainable.

---

## ✨ Features

- 🧠 **ReAct Agent** — LangGraph-based reasoning agent that thinks before acting
- 📧 **Gmail Auto-Reply** — IMAP listener reads unread emails, generates tickets, sends reply
- 🎫 **Smart Ticket Classification** — Auto-detects category, priority, subject from free-text
- 🔍 **Optional Web Search** — Tavily search tool for agents that need real-time info
- 🌐 **Multi-language** — Understands both English and Urdu input
- ⚡ **Groq Speed** — Llama 3 on Groq for ultra-fast inference
- 🔧 **FastAPI Backend** — REST endpoints for ticket creation, listing, and health check
- 📊 **SonarQube** — Static code analysis for code quality & security
- 🚀 **Jenkins Pipeline** — Automated CI/CD for build, test, and deploy

---

## 🏗️ System Architecture

```
User Email (Gmail)
      │
      ▼
┌─────────────────────┐
│   IMAP Listener     │  ← Polls every 30s for UNSEEN emails
└────────┬────────────┘
         │ Subject + Body
         ▼
┌─────────────────────────────────────────────┐
│           LangGraph ReAct Agent             │
│  ┌──────────────┐    ┌──────────────────┐   │
│  │  Groq LLM    │◄──►│  create_ticket   │   │
│  │  (Llama 3)   │    │  tool            │   │
│  └──────────────┘    └──────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │  Optional: Tavily Web Search Tool    │   │
│  └──────────────────────────────────────┘   │
└─────────────┬───────────────────────────────┘
              │ Structured Ticket (JSON)
              ▼
┌─────────────────────┐
│   FastAPI Backend   │  ← Saves to DB, returns ticket
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   SMTP Auto-Reply   │  ← Sends reply with ticket ID
└─────────────────────┘
```

---

## 🗂️ Project Structure

```
multi-ai-agent-using-sonarqube-jenkins/
│
├── app/
│   ├── config/
│   │   └── settings.py          # Env variables (Groq, Tavily keys)
│   ├── api/
│   │   └── routes.py            # FastAPI endpoints
│   └── models/
│       └── ticket.py            # Pydantic ticket model
│
├── ai_agent.py                  # Core ReAct agent (LangGraph + Groq)
├── itsm_agent.py                # ITSM-specific agent with ticket tool
├── email_listener.py            # Gmail IMAP listener + SMTP auto-reply
│
├── Jenkinsfile                  # CI/CD pipeline config
├── sonar-project.properties     # SonarQube config
├── requirements.txt
├── .env.example                 # Template (never commit actual .env)
├── .gitignore
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|------------|
| LLM | Llama 3 (via Groq API) |
| Agent Framework | LangGraph (ReAct pattern) |
| Web Search | Tavily Search API |
| Backend | FastAPI + Uvicorn |
| Email | Gmail IMAP + SMTP |
| Code Quality | SonarQube |
| CI/CD | Jenkins |
| Language | Python 3.10+ |

---

## 🚀 Quick Start

### 1. Clone karo
```bash
git clone https://github.com/mtoqeer-shahzad/multi-ai-agent-using-sonarqube-jenkins.git
cd multi-ai-agent-using-sonarqube-jenkins
```

### 2. Virtual environment banao
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Dependencies install karo
```bash
pip install -r requirements.txt
```

### 4. Environment variables set karo
```bash
# .env file banao (kabhi GitHub pe push mat karna)
cp .env.example .env
```

`.env` file fill karo:
```env
GROQ_API_KEY=gsk_your_groq_key_here
TAVILY_API_KEY=tvly_your_tavily_key_here
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
```

> ⚠️ Gmail App Password: Gmail → Settings → Security → 2-Step Verification → App Passwords

### 5. FastAPI server chalao
```bash
uvicorn app.main:app --reload
```
API docs: http://localhost:8000/docs

### 6. Email listener chalao
```bash
python email_listener.py
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/generate-ticket` | Ticket generate karo |
| `GET` | `/tickets` | Sare tickets list karo |
| `GET` | `/tickets/{id}` | Single ticket fetch karo |
| `GET` | `/health` | Server status check |

### Example Request
```bash
curl -X POST http://localhost:8000/generate-ticket \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Mera laptop screen black ho gaya hai",
    "requester_name": "Ali Hassan"
  }'
```

### Example Response
```json
{
  "ticket_id": "TKT-A1B2C3D4",
  "subject": "Laptop screen not working",
  "category": "Hardware",
  "priority": "High",
  "description": "User reports laptop screen has gone black and device is unresponsive.",
  "requester": "Ali Hassan",
  "status": "open",
  "created_at": "2025-01-15T10:30:00Z"
}
```

---

## 🔬 How the Agent Works

```python
# ai_agent.py — core pattern
llm   = ChatGroq(model=model_id, api_key=settings.GROQ_API_KEY)
tools = [TavilySearchResults(...)] if allow_search else []

agent = create_react_agent(model=llm, tools=tools, prompt=system_prompt)

response = agent.invoke({"messages": [{"role": "user", "content": query}]})

# Last AIMessage = final answer
ai_messages = [m.content for m in response["messages"] if isinstance(m, AIMessage)]
return ai_messages[-1]
```

The agent follows the **ReAct (Reason + Act)** loop:
1. **Reason** — "User ne kya problem batai?"
2. **Act** — Tool call karo (ticket create / web search)
3. **Observe** — Tool ka result dekho
4. **Repeat** — Jab tak final answer na mile

---

## 🔧 Jenkins CI/CD Pipeline

```groovy
// Jenkinsfile stages:
// 1. Checkout code
// 2. Install dependencies
// 3. Run tests (pytest)
// 4. SonarQube analysis
// 5. Build Docker image
// 6. Deploy to server
```

---

## 📊 SonarQube Code Quality

```properties
# sonar-project.properties
sonar.projectKey=multi-ai-agent
sonar.sources=.
sonar.language=py
sonar.python.version=3.10
```

Run analysis:
```bash
sonar-scanner
```

---

## 🔐 Security Best Practices

- ✅ `.env` file `.gitignore` mein add hai — kabhi push nahi hoga
- ✅ `.env.example` template GitHub pe available hai
- ✅ Gmail App Password use karo — actual Gmail password nahi
- ✅ API keys sirf environment variables se load hoti hain
- ✅ SonarQube secret detection enabled hai

---

## 📦 Requirements

```
fastapi
uvicorn
langchain-groq
langchain-community
langgraph
langchain-core
tavily-python
pydantic-settings
python-dotenv
```

---

## 👤 Author

**Muhammad Toqeer Shahzad**
AI/ML Engineer | LLM Systems | RAG Pipelines | Agentic AI

[![GitHub](https://img.shields.io/badge/GitHub-mtoqeer--shahzad-black?style=flat-square&logo=github)](https://github.com/mtoqeer-shahzad)

---

## 📄 License

MIT License — free to use, modify, and distribute.
