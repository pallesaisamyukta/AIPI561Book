# Use the official Python image from the Docker Hub
FROM python:3.7-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose port 5050 for the Flask app
EXPOSE 5050

# Define the command to run the Flask app
CMD ["python", "app.py"]

