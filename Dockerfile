# No dependencies — the backend is Python standard library only.
FROM python:3.12-alpine
WORKDIR /app
COPY server.py .
# State is written to /data; mount a volume there to persist it.
VOLUME ["/data"]
EXPOSE 8000
CMD ["python", "server.py"]
