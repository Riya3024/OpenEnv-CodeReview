TASKS = [
    {
        "code": "def add(a, b): return a + b",
        "expected": {"bug_type": "none"},
        "difficulty": "easy"
    },
    {
        "code": "def divide(a, b): return a / b",
        "expected": {"bug_type": "runtime_error"},
        "difficulty": "medium"
    },
    {
        "code": "def process(data): for i in data print(i)",
        "expected": {"bug_type": "syntax_error"},
        "difficulty": "hard"
    }
]