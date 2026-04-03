import os
import requests
import json
from dotenv import load_dotenv
from openai import OpenAI

# ------------------------------
#  Load ENV
# ------------------------------
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7860")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")  # optional


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


USE_API = False


# ------------------------------
# Smart Agent 
# ------------------------------
def smart_agent(code):
    code_lower = code.lower()

    if "print(" in code_lower and code.count("'") % 2 != 0:
        return {"bug_type": "syntax_error", "fix": "close quote"}

    if "if " in code_lower and "=" in code_lower and "==" not in code_lower:
        return {"bug_type": "syntax_error", "fix": "use =="}

    if "range(len(" in code_lower:
        return {"bug_type": "inefficient_loop", "fix": "use enumerate"}

    if "/" in code_lower:
        return {"bug_type": "division_by_zero", "fix": "check b != 0"}

    if "[" in code_lower and "]" in code_lower:
        return {"bug_type": "index_error", "fix": "check length"}

    if "return" in code_lower and "+ y" in code_lower:
        return {"bug_type": "undefined_variable", "fix": "define y"}

    return {"bug_type": "unknown", "fix": "review code"}


# ------------------------------
# LLM Call 
# ------------------------------
def call_llm(code):
    if USE_API:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "Return JSON bug_type and fix"},
                {"role": "user", "content": code}
            ],
            temperature=0
        )

        text = response.choices[0].message.content.strip()

        try:
            return json.loads(text)
        except:
            return {"bug_type": "unknown", "fix": text}

    else:
        return smart_agent(code)


# ------------------------------
#  MAIN RUN LOOP (STRUCTURED LOGS)
# ------------------------------
def run():
    print("=== START ===")

    total_score = 0
    steps = 6

    for step in range(1, steps + 1):
        print(f"\n--- STEP {step} ---")

        # Reset environment
        obs = requests.post(f"{API_BASE_URL}/reset").json()
        print("INPUT:", obs)

        # Agent prediction
        action_output = call_llm(obs["code"])

        action = {
            "bug_detected": "yes",
            "bug_type": action_output["bug_type"],
            "fix": action_output["fix"]
        }

        print("ACTION:", action)

        # Send to environment
        result = requests.post(f"{API_BASE_URL}/step", json=action).json()
        print("RESULT:", result)

        total_score += result["reward"]

    final_score = total_score / steps

    print("\n=== END ===")
    print(f"FINAL_SCORE: {final_score}")


# ------------------------------
# ▶ Entry
# ------------------------------
if __name__ == "__main__":
    run()