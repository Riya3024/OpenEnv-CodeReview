from pydantic import BaseModel

class Observation(BaseModel):
    code: str
    task_type: str
    difficulty: str


class Action(BaseModel):
    bug_detected: str
    bug_type: str
    fix: str


class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: dict