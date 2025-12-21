## 20 December 2025

### Day 2: Docker Compose + PostreSQL 
Let's solve that database connection issue and get your API fully working!

**Part 1: What is Docker Compose ?**
The Problem We're Solving:

Right now you have:
- ✅ Django app in a container
- ❌ PostgreSQL on your Ubuntu host (containers can't reach it)

What you need:
- Django Container 
- PostgreSQL container 
- Both containers talking to each other 

**Running them manually would be a NIGHTMARE:**
```bash
# Create network
docker network create my-network

# Run PostgreSQL
docker run -d --name postgres --network my-network \
  -e POSTGRES_PASSWORD=mypass -e POSTGRES_DB=mydb postgres:15

# Run Django
docker run -d --name django --network my-network \
  -p 8000:8000 -e DB_HOST=postgres lms-api-project:v2

# This is tedious and error-prone!
```

Docker Compose to the rescue:
One YAML file defines ALL your services (containers) and Docker Compose manages them together.
```yaml
# docker-compose.yml - one file to rule them all 
services:
    django:
    # django config

    postgres:
    # PostgreSQL config 
```
```bash
docker-compose up
```
Boom! Everything runs together.

**Part 2: Understanding docker-compose.yml structure** 
Basic Structure:
```yaml
version= '3.8'
services:           # Define all containers here  
    service1:       # Name of first service 
    # Config

    service2:       # Name of second service 
    # Config
        
volumes :   # Persistent data storage (optional)
    volumne1:  

networks:   # Custom Networks (optional)
    network1: 
```

Complete docker-compose.yml for your Django + PostgreSQL Setup :
Create a file named `docker-compose.yml` in your project root (same directory as `Dockerfile`):
```yaml
version = '3.8'
services: 
    # PostgreSQL Database Service 
    db: 
        image: postgres:15-alphine
        container_name: lms_postgres
        restart: unless-stopped 
        environment:   # below add your credential 
            POSTGRES_DB: lms_database
            POSTGRES_USER: lms_user 
            POSTGRES_PASSWORD: lms_password_123
        volumes :
            - postgres_data:/var/lib/postgresql/data
        ports:
            - "5432:5432"
        healthcheck:
            test: ["CMD-SHELL", "pg_isready -U lms_user -d lms_database"]
            interval: 10s
            timeout: 5s 
            retries: 5 
    
    # Django API Service 
    web:
    build: .
    container_name: lms_django
    command: >
      sh -c "python manage.py migrate &&
             python manage.py runserver 0.0.0.0:8000"
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    environment:
      - DB_NAME=lms_database
      - DB_USER=lms_user
      - DB_PASSWORD=lms_password_123
      - DB_HOST=db
      - DB_PORT=5432
      - DEBUG=True
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

**Part 3: Breaking Down Every Line**
Let me explain Every Single Thing:

**Section 1: Version** 
`version: '3.8'`

- Specifies Docker Compose file format version 
- '3.8' is stable and widely supported
- Different versions have different features 

**Section 2: PostgreSQL Service (db)**
```yaml
services:
    db:
        image: postgres:15-alphine
```

Explanation:
- `services:` = Define all containers 
- `db:` = Service name (you can call it anything: database, postgres, mydb)
- `image:` = Use Official PostgreSQL 15 with Alphine Linux (smallest version)
- We're NOT building this - just pulling from Docker Hub 

```yaml 
container_name: lms_postgres
```

Explanation:
- Give the container a readable name
- Without this, Docker auto-generates ugly names like "project_db_1" 
- Makes it easier to identify: `docker ps` will show "lms_postgres"

<br> 

```yaml
restart: unless-stopped 
```


Explanation :
- If container crashes, automatically restart it
- `unless-stopped` = restart on crash, but NOT If you manually stopped it.
- Other options: `no`, `always`, `on-failure`

<br> 

```yaml
environment:
    POSTGRES_DB: lms_database
    POSTGRES_USER: lms_user
    POSTGRES_PASSWORD: lms_password_123
```

Explanation:
- Environment variables passed to PostgreSQL container
- POSTGRES_DB = Creates database named "lms_database"
- POSTGRES_USER = Creates user "lms_user"
- POSTGRES_PASSWORD = Sets password "lms_password_123"
- These are used by PostgreSQL image to initialize the database 


```yaml 
volumes: 
    - postgres_data:/var/lib/postgresql/data
```

Explanation:
- Critical for Data Persistence
- Without this, if container stops, ALL DATABASE DATA IS LOST!
- `postgres_data` = Named volume (defined at bottom of file)
- `/var/lib/postgresql/data` = Where PostgreSQL stores data inside container 
- This maps the named volume to that location
- Data survives container restarts/deletions 

**Analogy:**
* Container = Your computer's RAM (temporary)
* Volume = Your computer's hard drive (permanent)

```yaml
ports:
  - "5432:5432"
``` 

Explanation :
- Expose PostgreSQL to your host machine
- Format: "HOST_PORT:CONTAINER_PORT"
- 5432 = PostgreSQL default port 
- Allows you to connect with tools like pgAdmin, DBeaver from your Ubuntu 
- Django container doesn't need this - it talks directly via Docker network

```yaml
healthcheck: 
  test: ["CMD-SHELL", "pg_isready -U lms_user -d lms_database"]
  interval: 10s
  timeout: 5s
  retries: 5
```

Explanation:
- Checks if PostgreSQL is ACTUALLY ready (not just started)
- `test:` = Command to check health 
- `pg_isready` = PostgreSQL utility that check if DB accepts connections 
- `interval: 10s` = Check every 10 seconds
- `timeout: 5s` = Wait max 5 seconds for response
- `retries: 5` = Try 5 times before marking as unhealthy 
- Why this matters: Django might start before PostgreSQL is ready and crash


**Section 3: Django Service (web)**
```yaml
web:
    build: .
```

Explanation:
- `web:`= Service name for Django
- `build: .` = Build image from Dockerfile in current directory (`.`)
- Unlike PostgreSQL (which use pre-built image), we BUILD Django Image

```yaml
container_name: lms_django
```

Explanation: 
- Friendly name for the container 
- Shows as "lms_django" in `docker ps`

```yaml
command: >
sh -c "python manage.py migrate && 
python manage.py runserver 0.0.0.0:8000"
```

Explanation :
- OVERRIDES THE CMD in Dockerfile
- > = YAML multi-line string
- sh -c = Run shell command 
- && = Run second command only if first succeeds 
- Flow: 
  1. Run migrations (create/update database tables)
  2. Then start Django server 
- This ensures migrations run EVERY time container starts 

```yaml
volumes:
  - .:/app
  - static_volume:/app/staticfiles
  - media_volume:/app/media
```

Explanation:
**Volume 1:** `.:/app` (Bindd Mount)
- Maps your PROJECT DIRECTORY on Ubuntu to /app in container
- LIVE CODE RELOADING: Change code on Ubuntu → instantly reflects in container
- Perfect for development
- For production, remove this line (use code baked into image)

**Volume 2:** `static_volume:/app/staticfiles` (Named Volume)
- Stores Django static files (CSS, JS, Images from admin, DRF)
- Persists across container restarts 
- Shared between containers if needed 

**Volume 3:** `media_volume:/app/media` (Named Volume)
- Stores user-uploaded files (profile pics, documents, etc.)
- Must persist across restarts
- CRITICAL: Without this, uploaded files disappear on restart

```yaml
ports: 
 - "8000:8000"
```

Explanation: 
- Expose Django to your Ubuntu machine 
- Access at `http://localhost:8000`
- Format: `"YOUR_PORT:CONTAINER_PORT"`
- Want port 8001? Change to `"8001:8000"`

```yaml
environment: 
  - DB_NAME=lms_database
  - DB_USER=lms_user
  - DB_PASSWORD=lms_password_123
  - DB_HOST=db
  - DB_PORT=5432
  - DEBUG=True
```

Explanation:
- Environment variables for Django 
- CRITICAL: `DB_HOST=db`
  - NOT "localhost"!
  - `db` = the SERVICE NAME of PostgreSQL 
  - Docker Compose create automatic DNS 
  - Containers can reach each other by service name 

You'll use these in Django `settings.py`:
```python 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}
```
```yaml
depends_on:
    db:
        condition: service_healthy
```

Explanation: 
- Django waits for PostgreSQL to be HEALTHY before starting
- `depends_on:` = Define startup order 
- `condition: service_healthy` = wait for healthcheck to pass
- Prevents Django from crashing because DB isn't ready yet 

```yaml
restart: unless-stopped
```

Explanation: 
-  Auto-restart Django if it crashes 
-  Same as PostgreSQL setting

Section 4: Volumes
```yaml
volumes:
    postgres_data:
    static_volume:
    media_volume:
```

Explanation: 
- Define named volumes used above
- Docker create these volumes
- Data stored in `/var/lib/docker/volumes/` on your Ubuntu
- Persist even if containers are deleted 


