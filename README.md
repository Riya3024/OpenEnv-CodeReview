Description

An environment for detecting bugs in Python code using agent interactions.

🚀 Endpoints
🔹 POST /reset

Resets the environment and returns a new code sample.

Response:

{
  "code": "def foo(): print(x)"
}
🔹 POST /step

Submit a bug detection action.

Request:

{
  "bug_detected": "yes",
  "bug_type": "NameError",
  "fix": "Define variable x before using it"
}

Response:

{
  "reward": 1.0,
  "done": true
}
🔹 GET /state

Returns current environment state.

🧠 Tasks
Syntax errors
Logical bugs
Runtime issues
🐳 Run with Docker
docker build -t env .
docker run -p 7860:7860 env
🌐 Access

Once running, the environment is available at:
http://localhost:7860
