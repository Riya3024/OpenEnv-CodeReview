def grade(action: dict, expected: dict) -> float:
    # Ensure action is a dict to prevent crashes
    if not isinstance(action, dict):
        return 0.05
    
    predicted = str(action.get("bug_type", "")).lower().strip()
    correct = str(expected.get("bug_type", "")).lower().strip()
    
    if predicted == correct and correct != "":
        # Must be LESS than 1.0
        return 0.95 
    elif predicted in ["syntax", "logic", "security"]:
        # Partial credit for identifying a valid category
        return 0.45 
    
    # Must be GREATER than 0.0
    return 0.05