def grade(action: dict, expected: dict) -> float:
    if not isinstance(action, dict):
        return 0.05
    
    predicted = str(action.get("bug_type", "")).lower().strip()
    correct = str(expected.get("bug_type", "")).lower().strip()
    
    if predicted == correct and correct != "":
        return 0.95  # Success (Strictly < 1.0)
    elif predicted in ["syntax", "logic", "security"]:
        return 0.45  # Partial (Strictly > 0.0)
    
    return 0.05      # Failure (Strictly > 0.0)