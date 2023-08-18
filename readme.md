# Simple to-do list

## Project description

<details>
<summary>English</summary>

## What is this?
This is simple to-do web-app.

## Why is it good?
It has minimalistic design, simple logic and web-server to give static.

## What is under the hood?
The app is written with Flask, patched with gevent monkey
- Flask stack: Bootstrap, SQLAlchemy, WTForms
- Web server: Nginx gives static, solves "leaky bucket" problem
- Docker: Dockerfile for Flask app and Docker Compose for Flask/Nginx tandem

## How to install?
```docker compose build && docker compose up -d```


## Disclaimer
The app was originally written in the last year (2022). The current commit is the attempt to refactor code and enhance the app with asynchronous gevent and nginx.

</details>


<details>
<summary>Russian</summary>

## Что это?
Это простое приложение для создания списка задач.

## Почему это хорошо?
У приложения минималистичный дизайн, простая логика и веб-сервер, отдающий статику

## Что под капотом?
Приложение написано на Flask, пропатченном gevent monkey
- Flask стак: Bootstrap, SQLAlchemy, WTForms
- Веб сервер: Nginx отдает статику и решает проблему "leaky bucket"
- Докер: Dockerfile для Flask приложения and Docker Compose для тандема Flask/Nginx

## Как установить и запустить?
```docker compose build && docker compose up -d```


## Дисклеймер
Приложение было написано в прошлом году (2022). Текущий коммит - попытка рефакторинга кода и улучшения посредством добавления асинхронного gevent и прикручивания nginx.

</details>
