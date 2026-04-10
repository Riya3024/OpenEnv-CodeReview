import os
import json
import requests
from openai import OpenAI

# ---- CONFIGURATION ----
# These are provided automatically by the validator
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("HF_TOKEN")  # MUST use HF_TOKEN
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
ENV_URL = os.getenv("ENV_URL", "http://localhost:7860")

# ---- CLIENT SETUP ----
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

def run():
    # 1. [START] Log - Mandatory for the validator to start tracking
    start_log = {
        "task": "code-review",
        "env": "openenv",
        "model": MODEL_NAME
    }
    print(f"[START] {json.dumps(start_log)}")

    all_rewards = []
    
    # 2. INITIAL RESET
    # We call this once to get the first task (task_easy)
    try:
        res = requests.post(f"{ENV_URL}/reset", timeout=10).json()
        obs = res.get("observation", {})
    except Exception as e:
        print(f"Failed to connect to environment: {e}")
        return

    # 3. MAIN EVALUATION LOOP
    # We loop 3 times because you have 3 tasks (easy, medium, hard)
    for i in range(3):
        code_to_review = obs.get("code", "def foo(): pass")
        
        # Construct the prompt for the LLM
        prompt = (
            f"Review this code: {code_to_review}\n"
            "Identify the bug type as either 'syntax', 'logic', or 'security'.\n"
            "Return ONLY a JSON object like this: {\"bug_type\": \"...\"}"
        )
        
        # Call the LLM using the OpenAI client
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            raw_content = response.choices[0].message.content.strip()
            
            # Clean up markdown code blocks if the LLM includes them
            if "```json" in raw_content:
                raw_content = raw_content.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_content:
                raw_content = raw_content.split("```")[1].split("```")[0].strip()
                
            action = json.loads(raw_content)
        except Exception as e:
            # Fallback action if LLM fails or returns bad JSON
            action = {"bug_type": "unknown"}

        # 4. STEP THE ENVIRONMENT
        try:
            reply = requests.post(f"{ENV_URL}/step", json=action, timeout=10).json()
            reward = float(reply.get("reward", 0.05)) # Default to small positive if missing
            done = reply.get("done", False)
            obs = reply.get("observation", {}) # Update observation for the next task
        except Exception as e:
            reward = 0.05
            done = True

        all_rewards.append(reward)

        # 5. [STEP] Log - Mandatory for tracking progress
        step_log = {
            "step": i + 1,
            "action": action.get("bug_type", "unknown"),
            "reward": reward,
            "done": done
        }
        print(f"[STEP] {json.dumps(step_log)}")
        
        # Break the loop if the environment says we are finished
        if done:
            break

    # 6. [END] Log - Mandatory for final scoring
    # Calculate the average score across all tasks
    avg_score = sum(all_rewards) / len(all_rewards) if all_rewards else 0
    end_log = {
        "success": avg_score > 0.5,
        "score": round(avg_score, 2),
        "rewards": all_rewards
    }
    print(f"[END] {json.dumps(end_log)}")

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        # Final catch-all to prevent the validator from seeing a raw python crash
        error_end = {"success": False, "score": 0, "error": str(e)}
        print(f"[END] {json.dumps(error_end)}")