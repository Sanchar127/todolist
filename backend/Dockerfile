FROM python:3.9-slim

WORKDIR /app

# Copy requirements.txt and install dependencies
COPY ./backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the backend files
COPY ./backend /app

# Set environment variables, ports, and run the backend server
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
