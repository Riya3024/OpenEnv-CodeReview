def grade(action: dict, expected: dict) -> float:
    # 1. Robustness: Handle cases where action might be None or not a dict
    if not isinstance(action, dict):
        return 0.0
    
    # 2. Case-insensitive matching
    predicted = str(action.get("bug_type", "")).lower().strip()
    correct = str(expected.get("bug_type", "")).lower().strip()
    
    # 3. Scoring Logic
    if predicted == correct and correct != "":
        return 1.0
    
    # 4. Partial Credit (Crucial for "Meaningful Reward" criteria)
    elif predicted in ["syntax", "logic", "security"]:
        return 0.3  # Gave a valid category, but the wrong one
        
    return 0.0