def grade(action, expected):
    predicted = getattr(action, "bug_type", "unknown")
    fix = getattr(action, "fix", "").lower()
    correct = expected["bug_type"]

    score = 0.0

    # correct classification
    if predicted == correct:
        score += 0.7
    elif predicted != "unknown":
        score += 0.3

    # reward good fix description
    if correct in fix:
        score += 0.3

    return min(score, 1.0)