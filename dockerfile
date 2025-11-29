FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["python", "server.py"]
