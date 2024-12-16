# Base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy files
COPY skade-app.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5005

# Start the application
CMD ["python", "skade-app.py"]