FROM python:3.12-alpine

# Create a working directory
WORKDIR /app

# Copy requirements.txt (if you have one)
COPY requirements.txt ./

# Install dependencies
RUN pip install -r requirements.txt

# Copy your application code
COPY . .

# Expose the port for Flask app
EXPOSE 5003

# Set the command to run the application
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5003"]