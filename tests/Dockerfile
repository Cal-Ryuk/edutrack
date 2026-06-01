FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

RUN pip install selenium==4.18.1

WORKDIR /tests
COPY test_edutrack.py .

CMD ["python", "-m", "unittest", "test_edutrack", "-v"]
