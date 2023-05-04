FROM python:3.11.3-slim

WORKDIR /home/app

COPY . .

RUN pip install --no-cache --upgrade -r requirements.txt

EXPOSE 8880

CMD ["python3", "run.py"]
