from fastapi import FastAPI
from env.environment import CodeEnv
from env.models import Action

app = FastAPI()
env = CodeEnv()

@app.post("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: Action):
    return env.step(action)

@app.get("/state")
def state():
    return env.state()