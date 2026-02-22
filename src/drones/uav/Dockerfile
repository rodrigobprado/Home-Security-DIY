FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY uav/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY uav/mavlink_bridge.py /app/mavlink_bridge.py
COPY common /app/common

CMD ["python3", "/app/mavlink_bridge.py"]
