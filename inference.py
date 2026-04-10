import os
import requests
import json
from openai import OpenAI

# ---- MANDATORY ENV VARIABLES ----
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("HF_TOKEN")  # FIXED: Validator uses HF_TOKEN
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
ENV_URL = os.getenv("ENV_URL", "http://localhost:7860")

# ---- CLIENT SETUP ----
# Mandatory: Must use OpenAI client
client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def run():
    # 1. [START] Log - Mandatory Format
    start_log = {"task": "code-review", "env": "openenv", "model": MODEL_NAME}
    print(f"[START] {json.dumps(start_log)}")

    all_rewards = []
    
    # 2. Reset ONCE at the beginning
    try:
        res = requests.post(f"{ENV_URL}/reset", timeout=10).json()
        obs = res.get("observation", {})
    except Exception as e:
        print(f"Reset failed: {e}")
        return

    # 3. Loop through the 3 tasks
    for i in range(3):
        code = obs.get("code", "def foo(): pass")
        
        # LLM CALL
        prompt = f"Identify bug type (syntax, logic, or security): {code}. Return ONLY JSON: {{\"bug_type\": \"...\"}}"
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            content = response.choices[0].message.content.strip()
            # Clean possible markdown wrap
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            action = json.loads(content)
        except:
            action = {"bug_type": "unknown"}

        # STEP ENV
        try:
            reply = requests.post(f"{ENV_URL}/step", json=action, timeout=10).json()
            reward = float(reply.get("reward", 0.05))
            done = reply.get("done", False)
            obs = reply.get("observation", {}) # Get next task info
        except:
            reward = 0.05
            done = True

        all_rewards.append(reward)

        # 4. [STEP] Log - Mandatory Format
        step_log = {
            "step": i + 1,
            "action": action.get("bug_type", "unknown"),
            "reward": reward,
            "done": done
        }
        print(f"[STEP] {json.dumps(step_log)}")
        
        if done:
            break

    # 5. [END] Log - MANDATORY FOR SCORING
    avg_score = sum(all_rewards) / len(all_rewards) if all_rewards else 0
    end_log = {
        "success": avg_score > 0.5,
        "score": round(avg_score, 2),
        "rewards": all_rewards
    }
    print(f"[END] {json.dumps(end_log)}")

if __name__ == "__main__":
    run()