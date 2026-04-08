from fastapi import FastAPI
from env.environment import CodeEnv
from env.models import Action

app = FastAPI()

env = CodeEnv()


@app.post("/reset")
def reset():
    obs = env.reset()

    # ✅ IMPORTANT: return dict (NOT object)
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
        "reward": float(result.reward),   # ensure float
        "done": bool(result.done)
    }


@app.get("/")
def root():
    return {"status": "running"}