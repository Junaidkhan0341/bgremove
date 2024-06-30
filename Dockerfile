# Use the official Miniconda image as the base image for the build stage
FROM continuumio/miniconda3:23.5.2-0 as builder

# Install necessary system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      apt-transport-https \
      bash \
      build-essential \
      git && \
    rm -rf /var/lib/apt/lists/*

# Create a conda environment and install necessary packages
RUN conda create -n bgremover-env python=3.8 && \
    conda clean --all -y

# Activate the environment and install required packages
SHELL ["conda", "run", "-n", "bgremover-env", "/bin/bash", "-c"]
RUN conda install 'ffmpeg>=4.4.0' -c conda-forge && \
    conda install pytorch torchvision torchaudio cpuonly -c pytorch && \
    pip install 'llvmlite==0.32.1' 'more_itertools==8.7.0' 'numba==0.47.0' 'Pillow==8.1.1' 'urllib3==1.26.6' && \
    pip install Flask==2.3.3 backgroundremover==0.1.9 waitress==2.1.2 && \
    pip install --no-cache-dir .

# Final stage: Use a minimal Debian image for the runtime environment
FROM debian:bullseye-slim

# Copy the conda environment from the builder stage
COPY --from=builder /opt/conda /opt/conda
ENV PATH=/opt/conda/bin:$PATH

# Copy the Flask application code into the container
WORKDIR /app
COPY app.py /app
COPY requirements.txt /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 5000 for the API
EXPOSE 5000

# Set the entry point to run the Flask application with Waitress
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "app:app"]
