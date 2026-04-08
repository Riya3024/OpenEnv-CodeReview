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
        "difficulty": obs.difficulty,
        "task_id": obs.task_type   # 🔥 VERY IMPORTANT
    }


@app.post("/step")
def step(action: dict):
    action_obj = Action(**action)
    result = env.step(action_obj)

    return {
        "reward": float(result.reward),
        "done": bool(result.done)
    }


# 🔥 ADD THIS (IMPORTANT FOR VALIDATOR)
@app.get("/tasks")
def tasks():
    return {
        "tasks": TASKS,
        "num_tasks": len(TASKS)
    }


@app.get("/")
def root():
    return {"status": "running"}