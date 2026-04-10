def grade(action: dict, expected: dict) -> float:
    # 1. Handle missing/bad input
    if not isinstance(action, dict):
        return 0.01 # Minimal positive score
        
    predicted = str(action.get("bug_type", "")).lower().strip()
    correct = str(expected.get("bug_type", "")).lower().strip()
    
    # 2. Logic with "Strictly between 0 and 1" clamping
    if predicted == correct and correct != "":
        score = 0.95  # Not 1.0
    elif predicted in ["syntax", "logic", "security"]:
        score = 0.40  # Partial credit
    else:
        score = 0.05  # Not 0.0
        
    return score