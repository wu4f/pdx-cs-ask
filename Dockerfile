# Multi-stage build.  To build the container, you will need to supply your
# GOOGLE_API_KEY to load the vector database within the final container

# Use an official Python runtime as a parent image
FROM python:3.12-slim as builder

# Ingestion script needs GoogleAI embeddings to insert into vector database.
# Pull GOOGLE_API_KEY from arguments
ARG GOOGLE_API_KEY

# Set environment variable for ingestion script
ENV GOOGLE_API_KEY=$GOOGLE_API_KEY

# Ingestion script needs PATH_NAME on site to target crawl
# Pull PATH_NAME from arguments
ARG PATH_NAME

# Set environment variable for ingestion script
ENV PATH_NAME=$PATH_NAME

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Run ingestion script to populate vector database
RUN python loaddb.py

# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Copy application over
COPY --from=builder /app /app

# Copy package libraries over
COPY --from=builder /usr/local /usr/local

# Set working directory
WORKDIR /app

# Launch chainlit
CMD chainlit run --port $PORT --host 0.0.0.0 cl.py
