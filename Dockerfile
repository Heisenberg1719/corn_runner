# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir telebot requests schedule psutil

# Define environment variable (you should set TELEGRAM_BOT_TOKEN when running the container)
ENV NAME World

# Run main.py when the container launches
CMD ["python", "main.py"]
