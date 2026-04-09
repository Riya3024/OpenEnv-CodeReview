def grade(action, expected):
    # action is a dict
    predicted = action.get("bug_type", "unknown")
    correct = expected["bug_type"]

    if predicted == correct:
     reward = 0.95
    else:
     reward = 0.1

    return max(0.01, min(0.99, reward))