# Code Review OpenEnv

## Description
Environment for detecting bugs in Python code.

## Endpoints
- POST /reset
- POST /step
- GET /state

## Tasks
- Syntax errors
- Logical bugs
- Runtime issues

## Run
docker build -t env .
docker run -p 7860:7860 env