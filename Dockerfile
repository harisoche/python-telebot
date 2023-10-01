# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set environment variables for the bot token
ENV BOT_TOKEN=YOUR_BOT_TOKEN

# Create a directory for your bot code
WORKDIR /app

# Copy your bot code into the container
COPY . .
COPY .env .env
# Install any dependencies your bot requires
RUN pip install --no-cache-dir -r requirements.txt

# Run your bot when the container starts
CMD ["python", "main.py"]