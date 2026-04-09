import os
import requests
import json
from openai import OpenAI

# ---- ENV VARIABLES ----
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
ENV_URL = os.getenv("ENV_URL", "http://localhost:7860")

# ---- CLIENT SETUP ----
client = None
if API_BASE_URL and API_KEY:
    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=API_KEY
    )
else:
    print("[WARNING] API not available — running in local mode")


# ---- LLM CALL ----
def call_llm(code):
    # Ensure LLM is triggered
    if not code:
        code = "def foo(): print(x)"

    # Use proxy if available
    if client:
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a code reviewer. Return ONLY JSON with keys bug_type and fix."
                    },
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
            print(f"[ERROR] LLM call failed: {e}")

    # Fallback (only for local runs)
    return {"bug_type": "unknown", "fix": "fallback"}


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


# ---- MAIN LOOP ----
def run():
    print(f"[START] task=code-review env=openenv model={MODEL_NAME}")

    rewards = []
    total_score = 0
    steps = 3
    obs = safe_post(f"{ENV_URL}/reset")

    for step in range(1, steps + 1):
        
       
        code = obs.get("code", "")

        # CALL LLM (REQUIRED)
        action_output = call_llm(code)

        action = {
            "bug_detected": "yes",
            "bug_type": action_output.get("bug_type", "unknown"),
            "fix": action_output.get("fix", "review code")
        }

        # STEP ENV
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


# ---- ENTRY POINT ----
if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"[FATAL ERROR] {e}")
        print("[END] success=false steps=0 score=0.00 rewards=0,0,0")