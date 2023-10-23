# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Specify your e-mail address as the maintainer of the container image
LABEL maintainer="yourname@pdx.edu"

# Execute apt-get update and install to get Python's package manager
#  installed (pip)
RUN apt-get update -y
RUN apt-get install -y python3-pip tesseract-ocr libtesseract-dev ffmpeg poppler-utils libxml2-dev libxslt1-dev antiword unrtf flac lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig

# Copy the contents of the current directory into the container directory /app
COPY . /app

# Set the working directory of the container to /app
WORKDIR /app

# Install the Python packages specified by requirements.txt into the container
RUN pip install --user -r requirements.txt

# Set the program that is invoked upon container instantiation
ENTRYPOINT ["python3"]

# Set the parameters to the program
CMD ["app.py"]
