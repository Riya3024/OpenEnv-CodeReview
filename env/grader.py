def normalize(text):
    return text.lower().strip()

def grade(action, expected):
    score = 0.0

    bug_pred = normalize(action.bug_type)
    fix_pred = normalize(action.fix)

    bug_exp = normalize(expected["bug_type"])
    fix_exp = normalize(expected["fix"])

    # 1. Bug type match (strict + partial)
    if bug_exp == bug_pred:
        score += 0.5
    elif bug_exp in bug_pred:
        score += 0.3

    # 2. Fix match (keyword-based)
    fix_keywords = fix_exp.split()
    match_count = sum(1 for word in fix_keywords if word in fix_pred)

    if match_count == len(fix_keywords):
        score += 0.4
    elif match_count > 0:
        score += 0.2

    # 3. Quality bonus (non-empty + useful)
    if len(fix_pred) > 5:
        score += 0.1

    return min(score, 1.0)