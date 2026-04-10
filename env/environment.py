from env.tasks import TASKS
from env.grader import grade

class CodeEnv:
    def __init__(self):
        self.index = 0

    def reset(self):
        self.index = 0
        task = TASKS[self.index]
        return {
            "observation": {
                "code": task["code"],
                "task_type": "code_review",
                "difficulty": task["difficulty"]
            }
        }

    def step(self, action):
        if self.index >= len(TASKS):
            return {"observation": {}, "reward": 0.0, "done": True, "info": {}}

        task = TASKS[self.index]
        # Ensure action is a dict and score is a float
        score = float(grade(action, task["expected"]))

        self.index += 1
        done = bool(self.index >= len(TASKS))

        observation = {}
        if not done:
            next_task = TASKS[self.index]
            observation = {
                "code": next_task["code"],
                "task_type": "code_review",
                "difficulty": next_task["difficulty"]
            }

        return {
            "observation": observation,
            "reward": score,
            "done": done,
            "info": {"task_id": task["id"]}
        }