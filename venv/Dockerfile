# Start with a Python environment
FROM python:3.9-slim

# Set the folder inside the container
WORKDIR /app

# Copy your 'shopping list' and install it
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your code (app.py and templates)
COPY . .

# Open port 5000 for the web app
EXPOSE 5000

# Start the app
CMD ["python", "app.py"]