from fastapi import FastAPI
from env.environment import CodeEnv
from env.models import Action
from env.tasks import TASKS

app = FastAPI()

env = CodeEnv()


# ---- RESET ----
@app.post("/reset")
def reset():
    obs = env.reset()

    return {
        "code": obs.code,
        "task_type": obs.task_type,
        "difficulty": obs.difficulty
    }


# ---- STEP ----
@app.post("/step")
def step(action: dict):
    action_obj = Action(**action)

    result = env.step(action_obj)

    return {
        "reward": result.reward,
        "done": result.done
    }


# ---- STATE (VERY IMPORTANT) ----
@app.get("/state")
def state():
    return {
        "current_task": env.state(),
        "available_tasks": TASKS   # 🔥 THIS LINE FIXES YOUR ERROR
    }


# ---- ROOT ----
@app.get("/")
def root():
    return {"status": "running"}