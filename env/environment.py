import random
from env.tasks import TASKS
from env.models import Observation, StepResult, Action
from env.grader import grade


class CodeEnv:
    def __init__(self):
        self.task = None
        self.task_index = 0   # ✅ NEW

    def reset(self):
        # cycle through tasks instead of random
        self.task = TASKS[self.task_index]
        self.task_index = (self.task_index + 1) % len(TASKS)

        return Observation(
            code=self.task["code"],
            task_type=self.task["id"],   # MUST be unique
            difficulty=self.task["difficulty"]
        )

    def step(self, action: Action):
        expected = self.task["expected"]

        score = grade(action, expected)

        reward = max(0.01, min(0.99, score))

        return StepResult(
            observation=self.reset(),
            reward=reward,
            done=True,
            info={"expected": expected}
        )

    def state(self):
        return {
            "current_task": self.task,
            "total_tasks": len(TASKS)   # ✅ helps validator
        }