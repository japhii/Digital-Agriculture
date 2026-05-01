# Use an official lightweight Python image
FROM python:3.11-slim

# Install system dependencies required for ML packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set up a non-root user (Hugging Face Spaces requirement)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory
WORKDIR $HOME/app

# Copy the requirements file and install dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY --chown=user . $HOME/app

# Expose port 7860 (Default for Hugging Face Spaces)
EXPOSE 7860

# Run gunicorn with --preload so that import tracebacks are printed to the logs
CMD ["gunicorn", "--preload", "-b", "0.0.0.0:7860", "--timeout", "120", "--workers", "1", "app:app"]
