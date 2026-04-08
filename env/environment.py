from env.tasks import TASKS
from env.models import Observation, StepResult, Action
from env.grader import grade


class CodeEnv:
    def __init__(self):
        self.tasks = TASKS
        self.index = 0
        self.task = None

    def reset(self):
        # sequential tasks (IMPORTANT)
        self.task = self.tasks[self.index]
        self.index = (self.index + 1) % len(self.tasks)

        return Observation(
            code=self.task["code"],
            task_type=self.task["id"],   # UNIQUE TASK ID
            difficulty=self.task["difficulty"]
        )

    def step(self, action: Action):
        expected = self.task["expected"]

        score = grade(action, expected)
        reward = max(0.01, min(0.99, score))

        return StepResult(
            observation=Observation(
                code=self.task["code"],
                task_type=self.task["id"],
                difficulty=self.task["difficulty"]
            ),
            reward=reward,
            done=True,
            info={
                "task_id": self.task["id"],
                "expected": expected
            }
        )