# Use the official Python base image
FROM python:3.12.3-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Set up Python virtual environment
RUN python -m venv venv

# Activate the virtual environment and install the Python dependencies
RUN /bin/bash -c "source venv/bin/activate && pip install --no-cache-dir -r requirements.txt"

# Copy the application code to the working directory
COPY . .

# Run the classifier within the virtual environment
CMD ["/bin/bash", "-c", "source venv/bin/activate && python classifier.py"]