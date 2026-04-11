# Student Management Platform — Phase 5

## Overview

Containerize your student platform with **Docker** and switch from SQLite to **PostgreSQL** using **Docker Compose**.

---

## What Changes From Yesterday

| Yesterday (Phase 4) | Today (Phase 5) |
|---|---|
| Run with python manage.py runserver | Run inside a Docker container |
| SQLite database (file-based) | PostgreSQL database (containerized) |
| Dependencies installed manually | Dependencies packaged in the image |
| Only works on your machine's setup | Runs identically on any machine with Docker |

---

## Files Provided

| File | What to do |
|---|---|
| `Dockerfile` | Fill in the steps — comments guide you |
| `.dockerignore` | Ready to use — keeps your image clean |
| `.env.example` | Copy to `.env` and fill in values |
| `docker-compose.yml` | Fill in the TODOs — comments guide you |

---

## Part 1: Containerize with Docker (SQLite)

### 1.1 Complete the Dockerfile

Open the provided `Dockerfile` and fill in each step. The comments tell you what each line should do. You need 6 lines total.

### 1.2 Set up environment variables

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Update `settings.py` to read SECRET_KEY and DEBUG from environment:
```python
import os

SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-dev-key')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'
```

### 1.3 Build and run

```bash
docker build -t studentplatform .
docker run -p 8000:8000 --env-file .env studentplatform
```

Visit http://localhost:8000 — your app should work.

### 1.4 Notice the problem

Add some data via admin, then stop the container (Ctrl+C) and run it again. Your data is gone — SQLite lives inside the container's temporary filesystem.

---

## Part 2: Docker Compose with PostgreSQL

### 2.1 Install PostgreSQL driver

Add `psycopg2-binary` to your `requirements.txt`.

### 2.2 Update settings.py

Replace the DATABASES section to use environment variables:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'studentplatform'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

### 2.3 Update .env

Uncomment the DB_ variables in your `.env` file. Make sure `DB_HOST=db` — this matches the service name in docker-compose.yml.

### 2.4 Complete docker-compose.yml

Open the provided `docker-compose.yml` and fill in the TODOs. The comments tell you what each section needs.

The db service needs: environment variables, a volume, and a port.
The web service needs: ports, env_file, and depends_on.
Don't forget to declare the pgdata volume at the bottom.

### 2.5 Run it

```bash
docker-compose up --build
```

In a separate terminal:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### 2.6 Test persistence

1. Visit http://localhost:8000, log in, add students
2. Stop: `docker-compose down`
3. Start: `docker-compose up`
4. Data should still be there

---

## Checklist

- [ ] Dockerfile completed and builds successfully
- [ ] .dockerignore in place
- [ ] .env file created from .env.example
- [ ] settings.py reads SECRET_KEY and DEBUG from environment
- [ ] App runs with `docker run` (SQLite version works)
- [ ] psycopg2-binary added to requirements.txt
- [ ] settings.py DATABASES updated for PostgreSQL with env vars
- [ ] docker-compose.yml completed (db + web + volume)
- [ ] `docker-compose up --build` works
- [ ] Migrations run inside container
- [ ] Superuser created inside container
- [ ] Data persists across container restarts
- [ ] .gitignore includes .env

---

## Bonus Challenges

- [ ] **Health check** — add a healthcheck in docker-compose to verify Django responds
- [ ] **Static files** — add `RUN python manage.py collectstatic --noinput` to the Dockerfile
- [ ] **Multiple environments** — create separate compose files for dev and production
- [ ] **Rebuild speed** — optimise your Dockerfile layer ordering for fastest rebuilds

---

## When You're Done

```bash
git add .
git commit -m "Session 7: Docker, Compose, PostgreSQL"
git push
```

**Next session**: HTML, CSS, JavaScript, and DOM manipulation.
