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
        return {"observation": {}, "reward": 0.01, "done": True, "info": {}}

    task = TASKS[current_task_index]
    
    # Get reward and clamp it strictly between 0 and 1
    reward = float(grade(action, task["expected"]))
    if reward >= 1.0: reward = 0.99
    if reward <= 0.0: reward = 0.01
    
    current_task_index += 1
    done = current_task_index >= len(TASKS)
    
    obs = {}
    if not done:
        next_t = TASKS[current_task_index]
        obs = {
            "code": next_t["code"], 
            "difficulty": next_t["difficulty"],
            "task_id": next_t["id"]
        }

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