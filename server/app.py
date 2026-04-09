from fastapi import FastAPI

app = FastAPI()

TASKS = [
    {"code": "def add(a, b): return a + b", "expected": "none"},
    {"code": "def add(a, b): return a - b", "expected": "logical_error"},
    {"code": "def add(a, b): return a + b print(a)", "expected": "syntax_error"},
]

index = 0


@app.post("/reset")
def reset():
    global index
    index = 0

    task = TASKS[index]

    return {
        "code": task["code"],
        "task_type": "code_review",
        "difficulty": "medium"
    }


@app.post("/step")
def step(action: dict):
    global index

    task = TASKS[index]

    predicted = action.get("bug_type", "unknown")
    correct = task["expected"]

    if predicted == correct:
        score = 0.9
    elif predicted != "unknown":
        score = 0.5
    else:
        score = 0.2

    score = max(0.01, min(0.99, score))

    index += 1
    done = index >= len(TASKS)

    if not done:
        next_task = TASKS[index]
        observation = {
            "code": next_task["code"],
            "task_type": "code_review",
            "difficulty": "medium"
        }
    else:
        observation = {}

    return {
        "observation": observation,
        "reward": float(score),
        "done": done,
        "info": {}
    }


@app.get("/")
def root():
    return {"status": "ok"}


# 🔥 ADD THIS
def main():
    return app

if __name__ == "__main__":
    main()