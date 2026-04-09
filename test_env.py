import requests

url = "http://localhost:7860"

print(requests.post(f"{url}/reset").json())

print(requests.post(f"{url}/step", json={"bug_type": "none"}).json())
print(requests.post(f"{url}/step", json={"bug_type": "logical_error"}).json())
print(requests.post(f"{url}/step", json={"bug_type": "syntax_error"}).json())