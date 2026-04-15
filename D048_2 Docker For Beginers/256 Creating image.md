# Dockerizing Your Own Application: Build & Run

---

## The Goal

Up until now you've been pulling *other people's* images from Docker Hub. This section is about creating **your own** Docker image from scratch — taking a real Flask app, packaging it into a container, and running it locally.

---

## The Application Structure

The Flask app is intentionally minimal — the focus is the *containerization process*, not the app itself.

```
project/
├── app.py            ← Flask web application
├── requirements.txt  ← Python dependencies (just flask)
└── Dockerfile        ← Instructions to build the Docker image
```

**app.py**
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**requirements.txt**
```
flask
```

---

## Why `host='0.0.0.0'` Matters

This is a subtle but critical detail. When you run a server, it must declare *which network interfaces it listens on*:

| Host Value | What It Means | Accessible From |
|---|---|---|
| `127.0.0.1` | Loopback only | Same machine only |
| `0.0.0.0` | All interfaces | localhost, local IP, and crucially — **inside a container** |

Inside a Docker container, your app gets assigned an **internal container IP** (like `172.17.0.2`). If you bind to `127.0.0.1`, the app is invisible to the outside world — even through port mapping. Binding to `0.0.0.0` means the app says *"I'll accept connections from any IP"* — which is what allows port mapping to work.

> **Interview tip:** `0.0.0.0` is a common question. It means "listen on all available network interfaces."

---

## The Dockerfile — Explained Line by Line

```dockerfile
FROM python:3.8-alpine

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```

### `FROM python:3.8-alpine`
- Sets the **base image** — the bottom layer everything builds on
- `python:3.8` means Python 3.8 is pre-installed
- `alpine` is a minimal Linux distribution (~5MB) — keeps your image tiny
- Docker pulls this from Docker Hub automatically during build

### `COPY . /app`
- Copies **everything in your current local directory** (`.`) into a folder called `/app` inside the image
- This is how your `app.py` and `requirements.txt` get inside the container

### `WORKDIR /app`
- Sets the working directory inside the container to `/app`
- All subsequent commands (`RUN`, `CMD`) execute from this path
- Equivalent to `cd /app` inside the container

### `RUN pip install -r requirements.txt`
- Executes during the **image build phase** (not at runtime)
- Installs Flask and all dependencies into the image layer
- This layer gets cached — if `requirements.txt` doesn't change, Docker skips reinstalling on future builds

### `CMD ["python", "app.py"]`
- Executes when the **container starts** (not during build)
- Starts your Flask server inside the container
- Only one `CMD` is allowed per Dockerfile — it defines the container's main process

---

## The Build-Run Lifecycle

```
Dockerfile
    │
    │  docker build -t welcome-app .
    ▼
Docker Image  (stored locally)
    │
    │  docker run -p 5000:5000 welcome-app
    ▼
Docker Container  (running environment)
    │
    │  accessible at localhost:5000
    ▼
Your Browser  →  "Hello World"
```

---

## Building the Image

```bash
docker build -t welcome-app .
```

| Part | Meaning |
|---|---|
| `docker build` | Tells Docker to build an image from a Dockerfile |
| `-t welcome-app` | Tags (names) the image as `welcome-app` |
| `.` | The build context — look for the Dockerfile in the current directory |

**What happens step by step:**
1. Docker reads the Dockerfile top to bottom
2. Each instruction creates a new **layer**
3. Layers are cached — unchanged layers are reused on rebuilds (fast)
4. Final result is a complete, named image

Verify it built:
```bash
docker images
# Shows: welcome-app    latest    <id>    ~60MB
```

---

## Running the Container

```bash
docker run -p 5000:5000 welcome-app
```

Without `-d` (detached), logs print directly to your terminal — useful for debugging. You can then open a second terminal and run `docker ps` to confirm it's running.

### What the Port Mapping Does Here

```
Your Browser
     │
     │ requests localhost:5000
     ▼
Host Machine (port 5000)
     │
     │ port mapping bridges to container
     ▼
Container (port 5000)
     │
     │ Flask app bound to 0.0.0.0:5000
     ▼
Response: "Hello World"
```

Because `host='0.0.0.0'` was set in `app.py`, the app inside the container accepts the incoming connection forwarded by port mapping.

---

## Connecting This to Your Lambda Work

Your Lambda Dockerfile followed **exactly** this same pattern:

| Flask App Dockerfile | Your Lambda Dockerfile |
|---|---|
| `FROM python:3.8-alpine` | `FROM public.ecr.aws/lambda/python:3.12` |
| `COPY . /app` | `COPY main.py ${LAMBDA_TASK_ROOT}` |
| `WORKDIR /app` | `${LAMBDA_TASK_ROOT}` serves the same purpose |
| `RUN pip install -r requirements.txt` | `RUN pip install --no-cache-dir -r requirements.txt` |
| `CMD ["python", "app.py"]` | `CMD ["main.lambda_handler"]` |

The only difference: Flask uses a long-running HTTP server, while Lambda uses a handler function triggered by events. The containerization mechanics are identical.

---

## Complete Command Reference for This Workflow

```bash
# Build your image from a Dockerfile in the current directory
docker build -t <image-name> .

# Run with port mapping (foreground — see logs)
docker run -p HOST_PORT:CONTAINER_PORT <image-name>

# Run in detached mode (background)
docker run -d -p HOST_PORT:CONTAINER_PORT <image-name>

# Verify the container is running
docker ps

# Stop the container
docker stop <container-id>

# View all local images
docker images
```

---

## What's Next: Pushing to Docker Hub

Once you have a working local image, the next step is **publishing it** to Docker Hub so anyone on any machine can pull and run it with a single command:

```bash
docker push <your-dockerhub-username>/<image-name>
```

This is exactly what you did with AWS ECR — ECR is just a private Docker Hub living inside your AWS account. The push/pull mechanics are identical, just the registry URL differs.