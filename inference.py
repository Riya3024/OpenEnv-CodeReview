import os
import requests
import json
from openai import OpenAI

MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
OPENAI_KEY = os.getenv("OPENAI_KEY")
ENV_URL = os.getenv("ENV_URL", "http://localhost:7860")

# ---- CLIENT ----
client = None
if OPENAI_KEY:
    try:
        client = OpenAI(api_key=OPENAI_KEY)
    except Exception as e:
        print(f"[ERROR] Client init failed: {e}")


# ---- LLM CALL ----
def call_llm(code):
    # Try real LLM first
    if client:
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "Return JSON with bug_type and fix"},
                    {"role": "user", "content": code}
                ],
                temperature=0
            )

            text = response.choices[0].message.content.strip()

            try:
                return json.loads(text)
            except:
                return {"bug_type": "unknown", "fix": text}

        except Exception as e:
            print(f"[ERROR] LLM failed: {e}")

    # ---- fallback heuristic (IMPORTANT) ----
    try:
        if "SyntaxError" in code:
            return {"bug_type": "syntax_error", "fix": "Fix syntax issue"}

        if "import" not in code:
            return {"bug_type": "missing_import", "fix": "Add import statements"}

        if "=" in code and "==" not in code:
            return {"bug_type": "assignment_issue", "fix": "Check assignment logic"}

    except:
        pass

    return {"bug_type": "unknown", "fix": "review code"}


# ---- SAFE REQUEST ----
def safe_post(url, payload=None):
    try:
        if payload:
            res = requests.post(url, json=payload, timeout=10)
        else:
            res = requests.post(url, timeout=10)

        return res.json()

    except Exception as e:
        print(f"[ERROR] Request failed: {e}")
        return {"code": "", "reward": 0, "done": True}


# ---- MAIN ----
def run():
    print(f"[START] task=code-review env=openenv model={MODEL_NAME}")

    rewards = []
    total_score = 0
    steps = 3

    for step in range(1, steps + 1):
        obs = safe_post(f"{ENV_URL}/reset")
        code = obs.get("code", "")

        action_output = call_llm(code)

        action = {
            "bug_detected": "yes",
            "bug_type": action_output.get("bug_type", "unknown"),
            "fix": action_output.get("fix", "review code")
        }

        result = safe_post(f"{ENV_URL}/step", action)

        reward = float(result.get("reward", 0))
        done = result.get("done", True)

        rewards.append(f"{reward:.2f}")
        total_score += reward

        print(
            f"[STEP] step={step} action={action['bug_type']} "
            f"reward={reward:.2f} done={str(done).lower()} error=null"
        )

    final_score = total_score / steps
    success = final_score > 0.5

    print(
        f"[END] success={str(success).lower()} steps={steps} "
        f"score={final_score:.2f} rewards={','.join(rewards)}"
    )


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"[FATAL ERROR] {e}")
        print("[END] success=false steps=0 score=0.00 rewards=0,0,0")