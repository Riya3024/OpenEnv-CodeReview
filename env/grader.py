def grade(action, expected):
    predicted = action.get("bug_type", "unknown")
    correct = expected["bug_type"]

    # ✅ your original logic
    if predicted == correct:
        reward = 0.9
    elif predicted != "unknown":
        reward = 0.5
    else:
        reward = 0.2

    reward = max(0.01, min(0.99, reward))

    return reward