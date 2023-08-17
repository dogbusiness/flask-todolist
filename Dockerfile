FROM python:3.11-slim-bullseye as python

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./requirements .

RUN pip install --upgrade pip \
     && pip install -r requirements.txt --no-cache-dir

COPY . .

WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["python", "main.py"]
