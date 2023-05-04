# Build stage
FROM python:3.11.3-slim

COPY . .

RUN pip install --no-cache --upgrade -r requirements.txt

EXPOSE 8880

CMD ["python3", "run.py"]
