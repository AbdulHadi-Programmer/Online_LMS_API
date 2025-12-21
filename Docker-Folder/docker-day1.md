## 20 December 2025

### Today's Mission: 
1. Understand what Docker actually is and why you need it
2. Write a DockerFile for your Django/DRF project 
3. Build and run your API in a container locally

**Part 1: What the hell is Docker?**
The problem Docker solves:

You know that classic excuse: "But it works on my machine!"

Your Django app works perfectly on your laptop:
- Python 3.11 
- Specific version of Django, DRF, psycopg2
- Certain system dependencies 
- Environment variables set up just right 

Then you try to deploy it, and boom - version conflicts, missing dependencies, different OS behaviours.

**Docker's Solution:** 
Package your ENTIRE application environment into a container - a lightweight, isolated box that includes :

* Your code
* Python runtime
* All dependencies 
* System libraries 
* Configuration 

This container runs identically everywhere - your laptop, your server, your teammate's machine, anywhere.

`Key concept: `
1. Image: A blueprint / template (like a class in OOP)
2. Container: A running instance of an image (like an object/instance)
3. Dockerfile: Instructions to build an image 
4. Docker Compose: Tool to run multiple containers together (your Django app + PostgreSQL + Redis, etc)

Think of it like this: 
- Dockerfile = recipe
- Image = meal kit (packaged, ready to cook)
- Container = the actual cooked meal on the table 

**Part 2: Install Docker**
Install Docker Desktop:
- Windows/Mac: Download from docker.com 
- Linux: `sudo apt install docker.io docker-compose`

Verify Installation :
```bash
docker --version
docker-compose --version 
```

**Part 3: Write your First DockerFile** 
Let me show you a Dockerfile for a Django/DRF project. I'll explain every single line 
```dockerfile
# start from an official Python runtie as base image 
FROM python:3.11-slim

# Set environment variables (optional)
ENV pythonunbuffered=1 \ 
    pythondontwritebytecode=1

# Set work directory inside container 
WORKDIR /app

# Install system dependencies (needed for psycopg2, pillow, etc)
RUN apt-get update && apt-get install -y \ 
    postgresql-client \ 
    build-essential \
    libpg-dev \ 
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file 
COPY requirements.txt /app/

# Install Python Dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project 
COPY . /app/

# Expose port 8000 (Django Default)
EXPOSE 8000

# Run Django Development server 
CMD ["python", "manage.py" "runserver", "0.0.0.0:8000"]
```
**Part 4: Complete Docker Production ready in the project  ***
## Complete Understand with Explaination :
```dockerfile
# ============================================
# STAGE 1: Choose Base Image
# ============================================
FROM python:3.11-slim

# EXPLANATION:
# - FROM: Every Dockerfile starts with this
# - python:3.11-slim: Official Python image, lightweight version
# - "slim" = smaller size, no unnecessary tools
# - Alternative: python:3.11-alpine (even smaller but can have issues with some packages)
# - This image is Debian-based Linux, works everywhere


# ============================================
# STAGE 2: Set Environment Variables
# ============================================
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# EXPLANATION:
# PYTHONUNBUFFERED=1: 
#   - Forces Python to print output immediately
#   - Without this, you won't see logs in real-time
#   - Critical for debugging

# PYTHONDONTWRITEBYTECODE=1:
#   - Prevents Python from creating .pyc files
#   - Keeps container smaller and cleaner
#   - .pyc files are compiled Python (not needed in containers)

# PIP_NO_CACHE_DIR=1:
#   - Pip won't store cache
#   - Reduces image size

# PIP_DISABLE_PIP_VERSION_CHECK=1:
#   - Skip pip version check (faster builds)


# ============================================
# STAGE 3: Set Working Directory
# ============================================
WORKDIR /app

# EXPLANATION:
# - Creates /app directory inside container
# - All subsequent commands run from here
# - Like doing "cd /app" permanently
# - Your project will live at /app inside container


# ============================================
# STAGE 4: Install System Dependencies
# ============================================
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# EXPLANATION (line by line):
# apt-get update: 
#   - Refresh package lists (like "sudo apt update")

# apt-get install -y:
#   - -y = automatically say "yes" to prompts

# postgresql-client:
#   - Tools to connect to PostgreSQL
#   - Needed for psycopg2

# build-essential:
#   - Compilers and build tools
#   - Required to compile Python packages written in C

# libpq-dev:
#   - PostgreSQL development libraries
#   - Required for psycopg2 (PostgreSQL adapter for Python)

# gcc:
#   - GNU C Compiler
#   - Some Python packages need this to compile

# && rm -rf /var/lib/apt/lists/*:
#   - Clean up package lists after install
#   - Reduces image size
#   - Good practice to keep images small


# ============================================
# STAGE 5: Install Python Dependencies
# ============================================
COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# EXPLANATION:
# COPY requirements.txt /app/:
#   - Copy ONLY requirements.txt first
#   - Why separate from copying all code? DOCKER CACHING!
#   - If you change code but not requirements, Docker reuses cached layer
#   - Saves time on rebuilds

# pip install --upgrade pip:
#   - Get latest pip version
#   - Prevents compatibility issues

# pip install --no-cache-dir -r requirements.txt:
#   - Install all packages from requirements.txt
#   - --no-cache-dir: Don't store cache (smaller image)


# ============================================
# STAGE 6: Copy Project Code
# ============================================
COPY . /app/

# EXPLANATION:
# COPY . /app/:
#   - Copy EVERYTHING from current directory (your project root)
#   - Into /app/ inside container
#   - . = current directory (where Dockerfile is)
#   - /app/ = destination inside container

# Why copy requirements.txt separately first, then copy everything?
# DOCKER LAYER CACHING:
#   - Each instruction creates a "layer"
#   - If nothing changed in that layer, Docker reuses it
#   - Requirements change less often than code
#   - So Docker can skip reinstalling packages if only code changed


# ============================================
# STAGE 7: Expose Port
# ============================================
EXPOSE 8000

# EXPLANATION:
# - Documents which port your app uses
# - Does NOT actually publish the port (that's done with -p flag when running)
# - Just documentation for other developers
# - Django default is 8000


# ============================================
# STAGE 8: Create entrypoint script (optional but recommended)
# ============================================
# We'll create this as a separate file


# ============================================
# STAGE 9: Default Command
# ============================================
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# EXPLANATION:
# CMD: Command to run when container starts
# ["python", "manage.py", "runserver", "0.0.0.0:8000"]:
#   - JSON array format (preferred)
#   - Alternative format: CMD python manage.py runserver 0.0.0.0:8000

# 0.0.0.0:8000:
#   - 0.0.0.0 means "listen on all network interfaces"
#   - Without 0.0.0.0, Django only listens to 127.0.0.1 (localhost inside container)
#   - You won't be able to access it from outside
#   - CRITICAL for Docker

# NOTE: For production, you'd use:
# CMD ["gunicorn", "your_project.wsgi:application", "--bind", "0.0.0.0:8000"]

```

**Part 5-6: Build and Test**
**Step 1: Generate requirements.txt**
```bash
pip freeze > requirements.txt 
```
**Step 2: Create Dockerfile**
(use the complete version above)
**Step 3: Create .dockerignore**`
(use the template above)
**Step 4: Build the Image**
```bash
docker build -t my-django-api:v1 .
```
- `-t my-django-api:v1` Tag with name and version
- `.`: Build context (current directory)

**Step 5: Run the container**
docker run -p 8000:8000 my-django-api:v1
```bash
# synatx of container running
docker run -p HOST_PORT:CONTAINER_PORT image_name
```

## Question: Image vs Container 
This is a KEY concept. Let me explain with a clear analogy:

**Image = Recipe Book (Static)**
- Created by `docker build` command
- Stored on your disk 
- immutable (cannot be changed)
- Blueprint / template
- Like a class in OOP 

**Container = Cooked Meal (Active)**
- Created by `docker run` command
- Running instance of an image
- Has state (running, stopped, has data)
- Like an object/instance in OOP 

