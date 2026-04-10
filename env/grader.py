def grade(action: dict, expected: dict) -> float:
    # Handle non-dictionary actions
    if not isinstance(action, dict):
        return 0.01
        
    predicted = str(action.get("bug_type", "")).lower().strip()
    correct = str(expected.get("bug_type", "")).lower().strip()
    
    # Logic: Strictly between 0 and 1
    if predicted == correct and correct != "":
        return 0.99  # NOT 1.0
    elif predicted != "" and predicted != "unknown":
        return 0.50  # Partial credit
    
    return 0.01  # NOT 0.0