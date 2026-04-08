def grade(action, expected):
    predicted = getattr(action, "bug_type", "unknown")
    correct = expected["bug_type"]

    if predicted == correct:
        score = 0.9
    elif predicted != "unknown":
        score = 0.5
    else:
        score = 0.1

    # STRICT (0,1)
    return max(0.01, min(0.99, score))