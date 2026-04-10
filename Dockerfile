FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn requests openai python-multipart
EXPOSE 7860
# This starts the environment server
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]