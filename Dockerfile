# Base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the Python script and other necessary files
COPY hit_urls.py /app

# Install dependencies
RUN pip install requests schedule tqdm

# Command to run the Python script
CMD ["python", "hit_urls.py"]
