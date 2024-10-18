# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir requests schedule

# Define environment variable
ENV NAME World

# Run ping_service.py when the container launches
CMD ["python", "main.py"]
