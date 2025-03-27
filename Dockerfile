FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install debugpy

# Copy the rest of the application
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501
EXPOSE 5678

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"] 