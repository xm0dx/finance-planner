# finance-planner

A self-hosted personal **finance planner** — a single-page web app for laying out income, expenses, and savings goals, backed by a tiny persistence API so your plan is saved server-side.

> Public overview of the project. It runs as one of the apps in my [homelab](https://github.com/xm0dx/homelab).

![Python](https://img.shields.io/badge/Python-0f1620?style=flat-square&logo=python&logoColor=5BC0EB)
![JavaScript](https://img.shields.io/badge/JavaScript-0f1620?style=flat-square&logo=javascript&logoColor=5BC0EB)
![HTML5](https://img.shields.io/badge/HTML5-0f1620?style=flat-square&logo=html5&logoColor=5BC0EB)
![CSS3](https://img.shields.io/badge/CSS3-0f1620?style=flat-square&logo=css3&logoColor=5BC0EB)
![nginx](https://img.shields.io/badge/nginx-0f1620?style=flat-square&logo=nginx&logoColor=5BC0EB)

## What it does

- A clean, single-page planner UI for budgeting — income vs. expenses, savings targets, and what's left over.
- Changes persist to a small backend API, so the plan survives a refresh and follows you across devices.
- Served behind nginx on a private network — same-origin API calls, no third-party services.

## How it's built

```text
Browser  ──/──▶  nginx  ──/api/──▶  Python persistence service  ──▶  saved state
   │
   └── static single-page app (HTML / CSS / JavaScript)
```

- **Frontend:** hand-written HTML / CSS / JavaScript single-page app.
- **Backend:** a small Python service that stores and returns the plan state over a simple REST endpoint.
- **Serving:** nginx reverse-proxies `/api/` to the backend and serves the static page on the same origin.

## Run it

```bash
docker compose up --build
# open http://localhost:8080
```

The plan is saved to a Docker volume by the backend, so it survives restarts.

## Structure

```text
.
├── app/index.html      single-page app (HTML / CSS / JavaScript)
├── server.py           persistence API — stdlib only, atomic JSON writes
├── nginx.conf          serves the app + proxies /api/ on one origin
├── docker-compose.yml  backend + nginx
└── Dockerfile          backend image
```

## Tech

Python · JavaScript · HTML · CSS · nginx · Docker
