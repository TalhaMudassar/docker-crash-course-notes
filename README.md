# 🐳 Docker Crash Course Notes

Personal notes from the **[Docker for Machine Learning | Docker Crash Course](https://youtu.be/GToyQTGDOS4?si=cKyXzCPW_O2tJVyW)** one-shot by **CampusX**, combining instructor slide notes and my own hands-on practice notes. Compiled while covering Docker separately (my degree didn't include a dedicated DevOps/cloud elective), before continuing the Docker section of my FastAPI course.

## 📌 What's Inside

- Core Docker concepts (images, containers, registries, Dockerfile)
- Why Docker is needed (consistency, isolation, scalability)
- Docker Engine architecture (daemon, CLI, REST API)
- Hands-on walkthrough: pulling/running existing images
- Building a custom Dockerfile from scratch (Flask example)
- Pushing images to Docker Hub
- Common use cases (microservices, CI/CD, ML/AI deployment, etc.)

## 📖 Table of Contents

1. [What is Docker?](#what-is-docker)
2. [Why Do We Need Docker?](#why-do-we-need-docker)
3. [Docker Engine](#docker-engine)
4. [Docker Image](#docker-image)
5. [Dockerfile](#dockerfile)
6. [Docker Container](#docker-container)
7. [Docker Registry](#docker-registry)
8. [Hands-on: Pulling & Running Images](#hands-on-pulling--running-images)
9. [Hands-on: Building a Custom Image (Flask App)](#hands-on-building-a-custom-image-flask-app)
10. [Pushing an Image to Docker Hub](#pushing-an-image-to-docker-hub)
11. [Use Cases](#use-cases)
12. [Command Cheat Sheet](#command-cheat-sheet)

---

## What is Docker?

Docker is a platform that helps developers **build, share, and run** containerized applications — packaging an app with everything it needs (code, runtime, libraries, config) so it runs the same way anywhere.

## Why Do We Need Docker?

| Problem | Docker's Solution |
|---|---|
| **Consistency** — apps behave differently across dev/test/prod due to config & dependency drift | Containers bundle everything the app needs, so it runs identically everywhere |
| **Isolation** — multiple apps on one host clash (dependency conflicts, resource contention) | Each app gets its own isolated container environment |
| **Scalability** — scaling manually is slow and error-prone | Spin up multiple container instances quickly for horizontal scaling |

## Docker Engine

The **core runtime** that powers Docker, made up of three parts:

1. **Docker Daemon (`dockerd`)** — background service on the host; manages images, containers, networks, and volumes; listens for API requests.
2. **Docker CLI (`docker`)** — the command-line tool used to talk to the daemon (build images, run containers, etc.).
3. **REST API** — the interface between the CLI and the daemon; also lets developers automate Docker or integrate it into their own apps.

## Docker Image

A **lightweight, standalone, executable package** containing everything needed to run a piece of software.

**Components:**
- **Base Image** — starting point (`alpine`, `ubuntu`, `python`, `node`, etc.)
- **Application Code** — your actual app files
- **Dependencies** — libraries/frameworks the app needs
- **Metadata** — env vars, labels, exposed ports

**Lifecycle:** `Creation (docker build)` → `Storage (local/registry)` → `Distribution (push/pull)` → `Execution (run as container)`

## Dockerfile

A text file with step-by-step instructions to build an image. Each instruction creates a new image **layer**.

| Instruction | Purpose | Example |
|---|---|---|
| `FROM` | Base image | `FROM python:3.9-slim` |
| `LABEL` | Metadata | `LABEL version="1.0"` |
| `RUN` | Run a command at build time | `RUN pip install -r requirements.txt` |
| `COPY` | Copy files into the image | `COPY . /app` |
| `ENV` | Set environment variables | `ENV NAME World` |
| `WORKDIR` | Set the working directory | `WORKDIR /app` |
| `EXPOSE` | Document the listening port | `EXPOSE 5000` |
| `CMD` | Default command on container start | `CMD ["python", "app.py"]` |
| `VOLUME` | Mount point for external data | `VOLUME ["/data"]` |
| `ARG` | Build-time variable | `ARG VERSION=1.0` |

## Docker Container

A **running instance of an image** — lightweight, portable, and isolated. Containers are ephemeral; images are immutable.

## Docker Registry

A service that **stores and distributes** images (push/pull), versioned with **tags** (e.g. `myapp:1.0`, `myapp:latest`).

- **Docker Hub** — the default public registry ([hub.docker.com](https://hub.docker.com))
- **Private Registries** — self-hosted, for internal/secure use
- **Third-party** — AWS ECR, Google GCR, Azure ACR

---

## Hands-on: Pulling & Running Images

Test the installation:

```bash
# Pull the image from Docker Hub
docker pull hello-world

# Run it (creates a container)
docker run hello-world
```

Run someone else's app (e.g. a Streamlit app) without installing its dependencies:

```bash
docker pull tweakster24/lappy
docker run -p 8501:8501 tweakster24/lappy
```

**Port mapping (`-p HOST:CONTAINER`)** connects a port on your machine to a port inside the container — e.g. `-p 8501:8501` lets you open `http://localhost:8501` in your browser.

## Hands-on: Building a Custom Image (Flask App)

**Project structure:**

```
flask-table-app/
│
├── app.py
├── requirements.txt
├── Dockerfile
└── templates/
    └── index.html
```

**`app.py`** — a simple Flask app that generates a multiplication table:

```python
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    table_data = None
    number = None
    if request.method == "POST":
        try:
            number = int(request.form.get("number"))
            table_data = [(number, i, number * i) for i in range(1, 11)]
        except ValueError:
            pass
    return render_template("index.html", number=number, table=table_data)

if __name__ == "__main__":
    # host="0.0.0.0" is required for Docker port mapping to work!
    app.run(host="0.0.0.0", port=5000)
```

**`requirements.txt`:**

```
Flask==3.0.0
Werkzeug==3.0.0
```

**`Dockerfile`:**

```dockerfile
# 1. Base image (tip: use python:3.9-slim for a smaller image size)
FROM python:3.9

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy everything from the local folder into /app
COPY . /app

# 4. Install dependencies
RUN pip install -r requirements.txt

# 5. Document the port the container uses
EXPOSE 5000

# 6. Command that runs when the container starts
CMD ["python", "app.py"]
```

**Build & run:**

```bash
# Build the image (-t = name/tag, use your Docker Hub username)
docker build -t <your-dockerhub-username>/table .

# Run it — map local port 8888 to the container's port 5000
docker run -p 8888:5000 <your-dockerhub-username>/table
```

Visit `http://localhost:8888` to see it live.

## Pushing an Image to Docker Hub

```bash
# 1. Log in
docker login

# 2. Push the image
docker push <your-dockerhub-username>/table
```

Anyone can now run it with:

```bash
docker run -p 5000:5000 <your-dockerhub-username>/table
```

---

## Use Cases

- **Microservices Architecture** — each service runs independently in its own container
- **CI/CD** — consistent environments from dev → test → prod
- **Cloud Migration** — containerize apps for portable, consistent deployment
- **Scalable Web Applications** — easy horizontal scaling
- **Testing & QA** — reproducible test environments identical to production
- **Machine Learning & AI** — consistent runtime for training/inference, reproducible experiments
- **API Development & Deployment** — reliable, consistent, and fast API delivery

## Command Cheat Sheet

```bash
docker pull <image>                 # Download an image from a registry
docker run <image>                  # Run a container from an image
docker run -p HOST:CONTAINER <image># Run with port mapping
docker build -t <name> .            # Build an image from a Dockerfile in current dir
docker images                       # List local images
docker ps                           # List running containers
docker ps -a                        # List all containers (incl. stopped)
docker stop <container_id>          # Stop a running container
docker rm <container_id>            # Remove a container
docker rmi <image_id>               # Remove an image
docker login                        # Log in to Docker Hub
docker push <username>/<image>      # Push an image to a registry
```

---

## 📚 Source

- Video: [Docker for Machine Learning | Docker Crash Course — CampusX](https://youtu.be/GToyQTGDOS4?si=cKyXzCPW_O2tJVyW)
- Notes compiled from instructor slides + personal hands-on practice notes

## 🗺️ Roadmap

- [ ] Docker Compose (multi-container apps)
- [ ] Docker networking in depth
- [ ] Docker volumes for persistent ML datasets/models
- [ ] Containerizing an ML model serving API (FastAPI + Docker)
