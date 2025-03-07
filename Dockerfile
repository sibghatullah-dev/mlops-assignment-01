FROM python:3.12-slim

WORKDIR /app

# Copy only the requirements and install dependencies
COPY app/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app and pre-trained model
COPY app/app.py app.py
COPY app/model/ model/

# Expose port for the Flask server
EXPOSE 5000

# Run the Flask server
CMD ["python", "app.py"]