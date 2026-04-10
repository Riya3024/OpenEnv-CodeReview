TASKS = [
    {
        "code": "def add(a, b): return a + b",
        "expected": {"bug_type": "none"},
        "difficulty": "easy"
    },
    {
        "code": "def add(a, b): return a - b",
        "expected": {"bug_type": "logical_error"},
        "difficulty": "medium"
    },
    {
        "code": "def add(a, b): return a + b print(a)",
        "expected": {"bug_type": "syntax_error"},
        "difficulty": "hard"
    }
]