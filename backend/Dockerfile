# Backend: stdlib-only Python JSON API (no pip dependencies).
FROM python:3.12-alpine

WORKDIR /app
COPY server.py .

# Run as a non-root user
RUN adduser -D -u 10001 appuser
USER appuser

EXPOSE 8000
CMD ["python", "server.py"]
