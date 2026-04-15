# Docker Compose: Running Multi-Container Applications

---

## The Problem Docker Compose Solves

A real application is rarely just one process. A typical web app looks like this:

```
┌─────────────────────────────────────────────────┐
│              Your Application                    │
│                                                  │
│  ┌──────────────┐    ┌─────────┐   ┌─────────┐  │
│  │  Web App     │◄──►│  Redis  │   │  MySQL  │  │
│  │  (Flask)     │    │ (cache) │   │  (db)   │  │
│  └──────────────┘    └─────────┘   └─────────┘  │
│  Container 1         Container 2   Container 3   │
└─────────────────────────────────────────────────┘
```

Without Docker Compose, you'd have to manually:
- Build and run each container separately
- Figure out networking between them
- Remember every `docker run` flag for every service
- Start and stop them individually

**Docker Compose** lets you define the entire multi-container setup in a single `docker-compose.yml` file and manage it all with one command.

> **Official definition:** Docker Compose is a tool for defining and running multi-container Docker applications.

---

## The Project Structure

```
project/
├── app.py                ← Flask app using Redis
├── requirements.txt      ← flask, redis
├── Dockerfile            ← instructions for the web container
└── docker-compose.yml    ← orchestrates all containers together
```

---

## The Application

```python
# app.py
from flask import Flask
import redis

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)  # 'redis' = service name in compose

@app.route('/')
def hello():
    count = cache.incr('hits')
    return f'Hello Krish, I have seen you {count} times.'
```

Key point: the Redis host is `'redis'` — not an IP address. Docker Compose automatically creates a **shared network** between all services and lets them reach each other by their **service name**. This is one of Compose's most powerful features.

---

## The Dockerfile (with New Concepts)

```dockerfile
FROM python:3.7-alpine

WORKDIR /code

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Copy and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Start the app
CMD ["flask", "run"]
```

### Two New Instructions Explained

**`ENV` — Environment Variables**

```dockerfile
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
```

- Bakes key-value pairs into the image as environment variables
- Flask reads `FLASK_APP` to know which file to run
- Flask reads `FLASK_RUN_HOST` to know which network interface to bind to
- Your code accesses these with `os.environ.get("KEY")`
- Can be overridden at runtime without rebuilding the image

**`EXPOSE` — Documenting the Container Port**

```dockerfile
EXPOSE 5000
```

- Declares which port the container's application listens on
- This is **documentation** — it doesn't automatically publish the port
- The actual port binding still happens via `-p` in `docker run` or `ports:` in Compose
- Think of it as saying: *"this container expects port 5000 to be mapped"*

---

## The `docker-compose.yml` File

```yaml
version: '3.0'

services:
  web:
    build: .
    ports:
      - "8000:5000"
    image: web-app

  redis:
    image: redis

  mysql:
    image: mysql
```

### Breaking It Down

**`version`** — specifies the Compose file format version. Use `3.x` for modern projects.

**`services`** — the heart of the file. Each entry under `services` becomes a separate container.

| Field | What It Does |
|---|---|
| `build: .` | Build the image from the Dockerfile in the current directory |
| `image: web-app` | Name to assign to the built image |
| `ports: "8000:5000"` | Map host port 8000 → container port 5000 |
| `image: redis` | Pull the `redis` image directly from Docker Hub |

**Indentation is critical in YAML** — wrong indentation causes syntax errors. Each level is 2 spaces.

---

## How the Networking Works

Docker Compose automatically creates a private network and connects all services to it:

```
Docker Compose Network (auto-created)
┌─────────────────────────────────────┐
│                                     │
│  web  ◄──────────────────► redis   │
│  (reachable as "web")   (reachable  │
│                          as "redis")│
│                                     │
└─────────────────────────────────────┘
         │
         │ port 8000 exposed to host
         ▼
   localhost:8000
```

Services find each other by **service name** — no IP addresses needed. This is why `app.py` connects to Redis using `host='redis'`.

---

## The Key Commands

```bash
# Start all services (builds if needed, then runs)
docker compose up

# Start in detached mode (background)
docker compose up -d

# Stop all running containers (keeps images and data)
docker compose stop

# Stop AND remove containers, networks
docker compose down

# Rebuild images and restart (after code changes)
docker compose up --build

# View running containers managed by Compose
docker compose ps

# View logs from all services
docker compose logs

# View logs from a specific service
docker compose logs web
```

---

## `docker compose up` vs `docker run` — The Key Difference

| | `docker run` | `docker compose up` |
|---|---|---|
| **Scope** | One container | All services defined in yml |
| **Networking** | Manual | Auto-created between services |
| **Config location** | Command-line flags | `docker-compose.yml` |
| **Reproducibility** | Re-type every time | Committed to version control |
| **Use case** | Quick one-off containers | Full application stacks |

---

## The Limitation — and What's Next

Right now, if you change `app.py` and want the container to reflect that change, you have to:

1. `docker compose stop`
2. Remove the old images
3. `docker compose up` (full rebuild)

This is tedious during development. The solution is **Docker Volumes** — which mount your local code directory directly into the container so that file changes are reflected instantly without rebuilding.

```yaml
# Preview of what volumes look like in docker-compose.yml
services:
  web:
    build: .
    volumes:
      - .:/code    # mount current directory into /code in the container
```

With this, saving `app.py` in VS Code instantly updates the running container — no rebuild needed.

---

## Connecting to Your Lambda Work

Your Lambda setup was a **single-container** deployment — one image, one function. But in a real microservices architecture on AWS, Docker Compose's multi-container pattern maps directly to:

| Docker Compose | AWS Equivalent |
|---|---|
| Multiple services in `yml` | Multiple ECS tasks / Lambda functions |
| Service-name networking | AWS VPC / service discovery |
| `redis` service | AWS ElastiCache |
| `mysql` service | AWS RDS |
| `docker compose up` | `ecs deploy` / CDK deploy |

The mental model is identical — you're just swapping local containers for managed AWS services.