FROM python:3.12-slim

WORKDIR /app
COPY inventory_manager.py .

WORKDIR /data
VOLUME /data

CMD ["python", "/app/inventory_manager.py"]
