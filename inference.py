import os
import requests
import json
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

ENV_URL = os.getenv("ENV_URL", "http://localhost:7860")


def call_llm(code):
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


def run():
    task_name = "code-review"
    env_name = "openenv"

    print(f"[START] task={task_name} env={env_name} model={MODEL_NAME}")

    rewards = []
    total_score = 0
    steps = 3

    for step in range(1, steps + 1):
        obs = requests.post(f"{ENV_URL}/reset").json()
        code = obs["code"]

        action_output = call_llm(code)

        action = {
            "bug_detected": "yes",
            "bug_type": action_output.get("bug_type", "unknown"),
            "fix": action_output.get("fix", "review code")
        }

        result = requests.post(f"{ENV_URL}/step", json=action).json()

        reward = float(result["reward"])
        done = result["done"]

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
    run()