from fastapi import FastAPI
from env.tasks import TASKS
from env.grader import grade


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
    reward = grade(action, task["expected"])

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
    uvicorn.run(app, host="0.0.0.0", port=7860)