TASKS = [
    {
        "id": "task_easy",
        "code": "def add(a, b): return a + b",
        "expected": {"bug_type": "none"},
        "difficulty": "easy"
    },
    {
        "id": "task_medium",
        "code": "def add(a, b): return a - b",
        "expected": {"bug_type": "logical_error"},
        "difficulty": "medium"
    },
    {
        "id": "task_hard",
        "code": "def add(a, b): return a + b print(a)",
        "expected": {"bug_type": "syntax_error"},
        "difficulty": "hard"
    }
]