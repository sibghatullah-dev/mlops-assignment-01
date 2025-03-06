# Dockerfile
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy requirements and install them
COPY app/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app folder
COPY app/ app/

# Expose port
EXPOSE 5000

# Set the working directory to the app folder
WORKDIR /app/app

# Command to run the Flask app
CMD ["python", "app.py"]
