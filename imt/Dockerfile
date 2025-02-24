# ********* Stage 1: Build a base image *********
FROM python:3.12-slim AS builder

# Create the code directory
RUN mkdir /code
 
# Set the working directory inside the container
WORKDIR /code
 
# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 
 
# Upgrade pip
RUN pip install --upgrade pip

# Copy the Django project  and install dependencies
COPY requirements/base.txt  /code/
COPY requirements/docker.txt  /code/
 
# run this command to install all dependencies 
RUN pip install --no-cache-dir -r docker.txt

# ********* Stage 2: Users and Permissions ***********
FROM python:3.12-slim AS runner
 
RUN useradd -m -r appuser && \
    mkdir -p /code/logs && \
    chown -R appuser:appuser /code

# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set the working directory inside the container
WORKDIR /code

# Copy application code
COPY --chown=appuser:appuser . .

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
 
# Set the entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]