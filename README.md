# 🧠💻 Code Review AI using OpenEnv

## 🚀 Overview

This project implements a **Code Review AI Simulator** using the OpenEnv framework.  
It simulates a reinforcement learning environment where an agent analyzes code, detects bugs, and suggests fixes.

The system is designed to be:

- ✅ Fully reproducible  
- ✅ Deterministic (no randomness)  
- ✅ Dockerized for deployment  
- ✅ Compatible with OpenAI client requirements  

---

## 🎯 Problem Statement

Build an environment where an AI agent can:

- Analyze code snippets  
- Detect bugs  
- Suggest fixes  
- Receive rewards based on correctness  

---

## 🧩 System Architecture
streamlit_app.py → (UI Demo)
inference.py → (Agent Loop)
↓
FastAPI (main.py)
↓
Environment + Grader


---

## 🧠 Agent Design

The project uses a **hybrid approach**:

- ✔ OpenAI client included (for compatibility)
- ✔ Deterministic rule-based agent used for inference

### Why?

To ensure:
- reproducibility
- no API dependency
- stable evaluation

---

## 🔍 Supported Bug Types

- Syntax Error (`if x = 10`)
- Missing Quotes (`print('Hello)`)
- Undefined Variable (`x + y`)
- Index Error (`x[5]`)
- Inefficient Loop (`range(len(arr))`)
- Division by Zero (`a/b`)

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|--------|--------|------------|
| `/reset` | POST | Get new task |
| `/step`  | POST | Submit action |
| `/state` | GET  | Get state |

---

## 📊 Example Output
=== START ===

--- STEP 1 ---
INPUT: {...}
ACTION: {...}
RESULT: {...}

=== END ===
FINAL_SCORE: 1.0

---

## ⚙️ Setup Instructions

### 1️⃣ Install dependencies
pip install -r requirements.txt


### 2️⃣ Run backend
python -m uvicorn main:app --port 7860

### 3️⃣ Run inference (MAIN EVALUATION)
python inference.py

### 4️⃣ Run UI (optional demo)
python -m streamlit run streamlit_app.py

## 🐳 Docker Setup

### Build
docker build -t openenv .


### Run
docker run -p 7860:7860 openenv

## 🔐 Environment Variables

Create `.env` file:
API_BASE_URL=http://localhost:7860

MODEL_NAME=gpt-4o-mini
HF_TOKEN=dummy
OPENAI_API_KEY=dummy


---

## ☁️ Deployment

This project is ready for:

- Hugging Face Spaces (Docker)
- Local deployment using Docker
- API-based evaluation

---

## 🏆 Evaluation Criteria Covered

- ✅ OpenEnv API compliance  
- ✅ Structured logs (START / STEP / END)  
- ✅ Deterministic agent behavior  
- ✅ 3+ tasks with grading  
- ✅ Docker build support  
- ✅ Fast execution (<20 min)  

---

## 🧠 Key Design Decisions

- Used rule-based agent for reproducibility  
- Included OpenAI client for requirement compliance  
- Designed modular environment (reset/step/state)  
- Ensured compatibility with limited resources  


## 🚀 Features

- 🤖 Auto bug detection
- 📊 Reward-based evaluation
- 🎨 Interactive Streamlit UI
- 🐳 Docker support
- ⚡ Fast execution

## 📌 Future Improvements

- Reinforcement learning training loop
- LLM-based agent integration
- Multi-language support
- Performance dashboard

## 👨‍💻 Author

Developed as part of a hackathon submission.
