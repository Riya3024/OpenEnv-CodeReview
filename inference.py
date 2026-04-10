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
    print(f"[START] {json.dumps({'task': 'code-review', 'env': 'openenv', 'model': MODEL_NAME})}")
    
    res = requests.post(f"{ENV_URL}/reset").json()
    obs = res.get("observation", {})
    all_rewards = []
    
    for i in range(3):
        code = obs.get("code", "")
        prompt = f"Identify bug type (syntax/logic/security): {code}. Return ONLY JSON: {{\"bug_type\": \"...\"}}"
        
        resp = client.chat.completions.create(model=MODEL_NAME, messages=[{"role": "user", "content": prompt}])
        try:
            action = json.loads(resp.choices[0].message.content)
        except:
            action = {"bug_type": "unknown"}

        reply = requests.post(f"{ENV_URL}/step", json=action).json()
        reward = reply.get("reward", 0.05)
        all_rewards.append(reward)
        
        print(f"[STEP] {json.dumps({'step': i+1, 'action': action.get('bug_type'), 'reward': reward, 'done': reply.get('done')})}")
        if reply.get("done"): break
        obs = reply.get("observation", {})

    score = sum(all_rewards) / 3
    print(f"[END] {json.dumps({'success': score > 0.5, 'score': round(score, 2), 'rewards': all_rewards})}")

if __name__ == "__main__":
    run()
