import os
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

ENV_URL = "http://localhost:7860"

def call_llm(code):
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Return JSON with bug_type and fix"},
            {"role": "user", "content": code}
        ],
        temperature=0
    )

    text = response.choices[0].message.content
    return eval(text)


def run():
    print("START")

    total = 0
    steps = 6

    for i in range(steps):
        print(f"STEP {i+1}")

        obs = requests.post(f"{ENV_URL}/reset").json()
        code = obs["code"]

        print("INPUT:", code)

        action_output = call_llm(code)

        action = {
            "bug_detected": "yes",
            "bug_type": action_output["bug_type"],
            "fix": action_output["fix"]
        }

        print("ACTION:", action)

        result = requests.post(f"{ENV_URL}/step", json=action).json()

        print("RESULT:", result)

        total += result["reward"]

    print("END")
    print("FINAL_SCORE:", total / steps)


if __name__ == "__main__":
    run()