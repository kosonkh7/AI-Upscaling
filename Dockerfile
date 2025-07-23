# Stage 1: Build stage with CUDA 12.6 development environment
FROM nvidia/cuda:12.6.0-devel-ubuntu22.04 AS builder

# Set environment variables to non-interactive
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies including Python 3.12, git, and all required libraries for Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    software-properties-common \
    libgl1-mesa-glx libglib2.0-0 \
    libjpeg-dev zlib1g-dev \
    libfreetype6-dev libpng-dev \
    liblmdb-dev ffmpeg \
    build-essential git && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y --no-install-recommends \
    python3.12 python3.12-venv python3.12-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Make python3.12 the default python
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 && \
    update-alternatives --set python3 /usr/bin/python3.12

# Set working directory
WORKDIR /app

# Create and activate virtual environment
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Upgrade pip and setuptools inside the venv to handle Python 3.12 changes
RUN pip install --no-cache-dir --upgrade pip setuptools

# Install PyTorch, torchvision, torchaudio, and xformers for CUDA 12.6
RUN pip install --no-cache-dir \
    torch==2.7.1 torchvision==0.22.1 torchaudio==2.7.1 xformers \
    --index-url https://download.pytorch.org/whl/cu126

# Copy requirements file and install dependencies inside the venv
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Stage 2: Final production stage with CUDA 12.6 runtime
FROM nvidia/cuda:12.6.0-runtime-ubuntu22.04

# Set environment variables to non-interactive
ENV DEBIAN_FRONTEND=noninteractive

# Install Python 3.12 runtime and all required libraries for Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    software-properties-common \
    libgl1-mesa-glx libglib2.0-0 \
    libjpeg-dev zlib1g-dev \
    libfreetype6-dev libpng-dev \
    liblmdb-dev ffmpeg \
    && add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y --no-install-recommends python3.12 python3.12-venv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Make python3.12 the default python
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 && \
    update-alternatives --set python3 /usr/bin/python3.12

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

# Set working directory
WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /app/venv /app/venv

# Copy model weights separately to optimize caching
COPY --chown=app:app backend/model_weights/ ./backend/model_weights/

# Copy the rest of the backend and frontend code
COPY --chown=app:app backend/ ./backend
COPY --chown=app:app frontend/ ./frontend

# Switch to the non-root user and activate the virtual environment
USER app
ENV PATH="/app/venv/bin:$PATH"

# Set working directory to the backend folder
WORKDIR /app/backend

# Expose the port the app runs on
EXPOSE 8000

# Run the application using Gunicorn
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "app.main:app"]
