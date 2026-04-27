FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY statbotics_mcp ./statbotics_mcp

RUN pip install .

EXPOSE 8000

ENTRYPOINT ["statbotics-mcp"]
