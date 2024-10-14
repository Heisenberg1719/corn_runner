# Use the official Python image from DockerHub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt first for leveraging Docker cache
COPY requirements.txt /app/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 5000 for the FastAPI server
EXPOSE 5000

# Run the main application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
