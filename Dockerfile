# Base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the script into the container
COPY hit_urls.py /app

# Install dependencies
RUN pip install requests schedule

# Command to run the script
CMD ["python", "hit_urls.py"]
