FROM python:3.12.3-slim 

# Environment Variables 
ENV PYTHONUNBUFFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore


# Set Workdir inside container 
WORKDIR /app 

# Install system dependencies 
RUN apt-get update && apt-get install -y \ 
    postgresql-client \ 
    build-essential \
    libpq-dev \
    gcc \ 
    && rm -rf /var/lib/apt/lists/*

# Install the Project Requirement
COPY requirements.txt /app/

# Install Dependencies :
RUN pip install --upgrade --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy Project Code 
COPY . /app/

# Expose Port 
EXPOSE 8000 

# Default Command 
# CMD = ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD python manage.py migrate && \ 
    python manage.py runserver 0.0.0.0:8000 


# NOTE: For production, you'd use:
# CMD ["gunicorn", "your_project.wsgi:application", "--bind", "0.0.0.0:8000"]

