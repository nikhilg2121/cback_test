FROM python:3.11

# Set working directory
WORKDIR /app

# Install Flask and other dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the Flask application code
COPY . .


EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]