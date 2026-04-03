TASKS = [
    {
        "difficulty": "easy",
        "code": "if x = 10:\n print(x)",
        "expected": {"bug_type": "syntax_error", "fix": "use =="}
    },
    {
        "difficulty": "easy",
        "code": "print('Hello)",
        "expected": {"bug_type": "syntax_error", "fix": "close quote"}
    },
    {
        "difficulty": "medium",
        "code": "for i in range(len(arr)):\n print(arr[i])",
        "expected": {"bug_type": "inefficient_loop", "fix": "use enumerate"}
    },
    {
        "difficulty": "medium",
        "code": "x = [1,2,3]\nprint(x[5])",
        "expected": {"bug_type": "index_error", "fix": "check length"}
    },
    {
        "difficulty": "hard",
        "code": "def divide(a,b): return a/b",
        "expected": {"bug_type": "division_by_zero", "fix": "check b != 0"}
    },
    {
        "difficulty": "hard",
        "code": "def f(x): return x + y",
        "expected": {"bug_type": "undefined_variable", "fix": "define y"}
    }
]