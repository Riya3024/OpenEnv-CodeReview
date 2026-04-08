from env.tasks import TASKS
from env.models import Observation, StepResult, Action
from env.grader import grade




class CodeEnv:
    def __init__(self):
        self.task = None

    def reset(self):
        import random
        self.task = random.choice(TASKS)

        return Observation(
            code=self.task["code"],
            task_type="code_review",
            difficulty=self.task["difficulty"]
        )

    def step(self, action):
        expected = self.task["expected"]

        score = grade(action, expected)

        # ✅ STRICT BETWEEN (0,1)
        score = max(0.01, min(0.99, score))

        return StepResult(
            observation=Observation(
                code=self.task["code"],
                task_type="code_review",
                difficulty=self.task["difficulty"]
            ),
            reward=score,
            done=True,
            info={"expected": expected}
        )

    def state(self):
        return self.task