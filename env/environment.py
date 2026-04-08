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
            task_type="code_review",
            difficulty=self.task["difficulty"]
        )

    def step(self, action: Action):
        expected = self.task["expected"]

        score = grade(action, expected)

        # reward shaping
        reward = score

# penalty for bad answers
        if score < 0.3:
         reward -= 0.1

        reward = max(0.0, min(1.0, reward))

        return StepResult(
            observation=self.reset(),
            reward=reward,
            done=True,
            info={"expected": expected}
        )

    def state(self):
        return self.task