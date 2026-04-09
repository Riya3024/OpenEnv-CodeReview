from env.tasks import TASKS
from env.grader import grade


class CodeEnv:
    def __init__(self):
        self.index = 0

    def reset(self):
        self.index = 0
        task = TASKS[self.index]

        return {
            "code": task["code"],
            "task_type": "code_review",
            "difficulty": task["difficulty"]
        }

    def step(self, action):
        task = TASKS[self.index]

        score = grade(action, task["expected"])

        self.index += 1
        done = self.index >= len(TASKS)

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
            "info": {}
        }