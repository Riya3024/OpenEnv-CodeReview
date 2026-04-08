from fastapi import FastAPI
from env.tasks import TASKS
from env.grader import grade

app = FastAPI()

# global index for tasks
task_index = -1
current_task = None


@app.post("/reset")
def reset():
    global task_index, current_task

    # 🔥 FORCE DIFFERENT TASK EACH TIME
    task_index = (task_index + 1) % len(TASKS)
    current_task = TASKS[task_index]

    return {
        "code": current_task["code"],
        "task_type": current_task["id"],   # 🔥 CRITICAL
        "difficulty": current_task["difficulty"]
    }


@app.post("/step")
def step(action: dict):
    global current_task

    predicted = action.get("bug_type", "unknown")
    correct = current_task["expected"]["bug_type"]

    # grading
    if predicted == correct:
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