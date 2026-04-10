from fastapi import FastAPI
from env.tasks import TASKS

app = FastAPI()

index = 0


@app.post("/reset")
def reset():
    global index
    index = 0

    task = TASKS[index]

    return {
        "code": task["code"],
        "task_type": "code_review",
        "difficulty": task["difficulty"]
    }


@app.post("/step")
def step(action: dict):
    global index

    # ✅ Safety check (prevents crash)
    if index >= len(TASKS):
        return {
            "observation": {},
            "reward": 0.0,
            "done": True,
            "info": {}
        }

    task = TASKS[index]

    # ✅ Safe extraction
    predicted = action.get("bug_type", "unknown") or "unknown"
    correct = task.get("expected", {}).get("bug_type", "unknown")

    # ✅ Reward logic (dynamic + validator-friendly)
    if predicted == correct:
        reward = 0.9
    elif predicted != "unknown":
        reward = 0.5
    else:
        reward = 0.2

    # ✅ Clamp reward (IMPORTANT)
    reward = max(0.01, min(0.99, reward))

    # Move to next task
    index += 1
    done = index >= len(TASKS)

    # Next observation
    if not done:
        next_task = TASKS[index]
        observation = {
            "code": next_task["code"],
            "task_type": "code_review",
            "difficulty": next_task["difficulty"]
        }
    else:
        observation = {}

    return {
        "observation": observation,
        "reward": reward,
        "done": done,
        "info": {}
    }


@app.get("/")
def root():
    return {"status": "ok"}

def main():
    return app

# Optional (for local testing only)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)