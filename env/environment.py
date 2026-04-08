from env.tasks import TASKS
from env.models import Observation, StepResult, Action
from env.grader import grade


class CodeEnv:
    def __init__(self):
        self.tasks = TASKS
        self.index = -1
        self.task = None

    def reset(self):
        # 🔥 cycle through tasks EVERY reset
        self.index = (self.index + 1) % len(self.tasks)
        self.task = self.tasks[self.index]

        return Observation(
            code=self.task["code"],
            task_type=self.task["id"],   # MUST be unique per task
            difficulty=self.task["difficulty"]
        )

    def step(self, action: Action):
        expected = self.task["expected"]

        score = grade(action, expected)

        # STRICT (0,1)
        reward = max(0.01, min(0.99, score))

        return StepResult(
            observation=self.reset(),
            reward=reward,
            done=True,
            info={"task_id": self.task["id"]}
        )

    def state(self):
        return {
            "num_tasks": len(self.tasks)
        }