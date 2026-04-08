from fastapi import FastAPI
import hashlib

app = FastAPI()

TASKS = [
    {"id": "easy", "code": "def add(a, b): return a + b", "expected": "none"},
    {"id": "medium", "code": "def add(a, b): return a - b", "expected": "logical_error"},
    {"id": "hard", "code": "def add(a, b): return a + b print(a)", "expected": "syntax_error"},
]


@app.post("/reset")
def reset():
    # 🔥 generate unique task each call
    key = hashlib.md5().hexdigest()
    index = int(key, 16) % len(TASKS)

    task = TASKS[index]

    return {
        "code": task["code"],
        "task_type": task["id"],
        "expected": task["expected"]   # 🔥 CRITICAL
    }


@app.post("/step")
def step(action: dict):
    # 🔥 expected passed back from reset
    expected = action.get("expected", "unknown")
    predicted = action.get("bug_type", "unknown")

    if predicted == expected:
        score = 0.9
    elif predicted != "unknown":
        score = 0.5
    else:
        score = 0.2

    score = max(0.01, min(0.99, score))

    return {
        "reward": float(score),
        "done": True
    }


@app.get("/")
def root():
    return {"status": "running"}