import random
from env.tasks import TASKS
from env.models import Observation, StepResult, Action
from env.grader import grade


class CodeEnv:
    def __init__(self):
        self.task = None

    def reset(self):
        self.task = random.choice(TASKS)

        return Observation(
            code=self.task["code"],
            task_type=self.task["id"],   # ✅ FIX 1 (VERY IMPORTANT)
            difficulty=self.task["difficulty"]
        )

    def step(self, action: Action):
        expected = self.task["expected"]

        score = grade(action, expected)

        # reward shaping
        reward = score

        # STRICT RANGE (0,1) — NO ZERO
        reward = max(0.01, min(0.99, reward))   # ✅ FIX 2

        return StepResult(
            observation=self.reset(),
            reward=reward,
            done=True,
            info={"expected": expected}
        )

    def state(self):
        return self.task