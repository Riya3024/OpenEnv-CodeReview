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

    task = TASKS[index]

    predicted = action.get("bug_type", "unknown")
    correct = task.get("expected", {}).get("bug_type", "unknown")

    reward = 0.9 if predicted == correct else 0.2
    reward = max(0.01, min(0.99, reward))

    index += 1
    done = index >= len(TASKS)

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)