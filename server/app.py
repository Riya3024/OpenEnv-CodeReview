from fastapi import FastAPI, Request
from env.tasks import TASKS
from env.grader import grade
import uvicorn

app = FastAPI()
current_task_index = 0

@app.post("/reset")
async def reset(payload: dict = None):
    global current_task_index
    current_task_index = 0
    task = TASKS[current_task_index]
    return {
        "observation": {
            "code": task["code"],
            "difficulty": task["difficulty"],
            "task_id": task["id"]
        }
    }

@app.post("/step")
async def step(request: Request):
    global current_task_index
    
    try:
        action = await request.json()
    except:
        action = {}

    if current_task_index >= len(TASKS):
        return {"observation": {}, "reward": 0.01, "done": True}

    task = TASKS[current_task_index]
    
    # Get the score from our new grader
    raw_reward = grade(action, task["expected"])
    
    # EXTRA SAFETY: Force the score to stay between 0.01 and 0.99
    reward = max(0.01, min(0.99, float(raw_reward)))
    
    current_task_index += 1
    done = current_task_index >= len(TASKS)
    
    obs = {}
    if not done:
        next_t = TASKS[current_task_index]
        obs = {"code": next_t["code"], "difficulty": next_t["difficulty"], "task_id": next_t["id"]}

    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": {"task_id": task["id"]}
    }

@app.get("/")
def health():
    return {"status": "ok"}

def main():
    return app

# Optional (for local testing only)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)