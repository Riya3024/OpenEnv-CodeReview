from fastapi import FastAPI
from env.environment import CodeEnv
from env.models import Action
from env.tasks import TASKS

app = FastAPI()

env = CodeEnv()


@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "code": obs.code,
        "task_type": obs.task_type,
        "difficulty": obs.difficulty
    }


@app.post("/step")
def step(action: dict):
    action_obj = Action(**action)
    result = env.step(action_obj)

    return {
        "reward": result.reward,
        "done": result.done
    }


# 🔥 THIS FIXES YOUR ERROR
@app.get("/state")
def state():
    return {
        "available_tasks": TASKS,
        "num_tasks": len(TASKS)
    }


@app.get("/")
def root():
    return {"status": "running"}