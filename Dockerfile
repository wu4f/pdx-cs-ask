# Multi-stage build.  To build the container, you will need to supply your
# GOOGLE_API_KEY to load the vector database within the final container
#   docker build --build-arg GOOGLE_API_KEY=$GOOGLE_API_KEY -f Dockerfile -t wuchangfeng/pdx-cs-ask .

# Use an official Python runtime as a parent image
FROM python:3.10-slim as builder

# Ingestion script needs GoogleAI embeddings to insert into vector database.
# Pull GOOGLE_API_KEY from arguments
ARG GOOGLE_API_KEY

# Set environment variable for ingestion script
ENV GOOGLE_API_KEY=$GOOGLE_API_KEY

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run ingestion script to populate vector database
RUN python loaddb.py

# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Copy application over
COPY --from=builder /app /app

# Copy package libraries over
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/

# Set working directory
WORKDIR /app

# Launch gunicorn
CMD gunicorn --bind :$PORT --workers 1 --threads 8 app:app

#CMD python3 gunicorn --bind :$PORT --workers 1 --threads 8 app:app
