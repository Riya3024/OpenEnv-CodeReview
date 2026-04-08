import random
from env.tasks import TASKS
from env.models import Observation, StepResult, Action
from env.grader import grade


class CodeEnv:
    def __init__(self):
        self.tasks = TASKS
        self.task_index = 0
        self.task = None

    def reset(self):
        # deterministic cycling
        self.task = self.tasks[self.task_index]
        self.task_index = (self.task_index + 1) % len(self.tasks)

        return Observation(
            code=self.task["code"],
            task_type=self.task["id"],   # MUST be unique
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