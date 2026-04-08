import random
from env.tasks import TASKS
from env.models import Observation, StepResult, Action
from env.grader import grade


class CodeEnv:
    def __init__(self):
        self.tasks = TASKS
        self.task = None

    def reset(self, task_id=None):
        if task_id:
            # select specific task
            self.task = next(t for t in self.tasks if t["id"] == task_id)
        else:
            # default fallback
            self.task = self.tasks[0]

        return Observation(
            code=self.task["code"],
            task_type=self.task["id"],
            difficulty=self.task["difficulty"]
        )

    def step(self, action: Action):
        expected = self.task["expected"]

        score = grade(action, expected)

        reward = max(0.01, min(0.99, score))  # STRICT RANGE

        return StepResult(
            observation=self.reset(),
            reward=reward,
            done=True,
            info={"task_id": self.task["id"], "expected": expected}
        )

    def state(self):
        return {
            "tasks": self.tasks,   # 🔥 expose ALL tasks
            "current_task": self.task
        }