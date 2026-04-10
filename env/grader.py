def grade(action, expected):
    predicted = action.get("bug_type", "unknown")
    correct = expected["bug_type"]

    if predicted == correct:
        return 0.9
    else:
        return 0.1