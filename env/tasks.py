TASKS = [
    {
        "id": "task_easy",
        "code": "def hello(): print('Missing quote)",
        "difficulty": "easy",
        "expected": {"bug_type": "syntax"}
    },
    {
        "id": "task_medium",
        "code": "def find_max(numbers): return min(numbers)",
        "difficulty": "medium",
        "expected": {"bug_type": "logic"}
    },
    {
        "id": "task_hard",
        "code": "query = f'SELECT * FROM users WHERE id={user_input}'",
        "difficulty": "hard",
        "expected": {"bug_type": "security"}
    }
]