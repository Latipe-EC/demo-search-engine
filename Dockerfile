FROM python:3.10.14-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that the application will run on
EXPOSE 5505

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5505"]
