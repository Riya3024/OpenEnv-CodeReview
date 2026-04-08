def grade(action, expected):
    predicted = getattr(action, "bug_type", "unknown")
    fix = getattr(action, "fix", "").lower()
    correct = expected["bug_type"]

    score = 0.0

    # classification score
    if predicted == correct:
        score = 0.9
    elif predicted != "unknown":
        score = 0.5
    else:
        score = 0.1

    # bonus for good fix
    if correct in fix:
        score += 0.05

    # ensure STRICT range (0,1)
    score = max(0.01, min(0.99, score))

    return score