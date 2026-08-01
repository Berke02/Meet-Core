# syntax=docker/dockerfile:1

FROM python:3.11-slim AS builder

ARG INSTALL_AUDIO=true

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    VIRTUAL_ENV=/opt/venv

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        build-essential \
        git \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv "${VIRTUAL_ENV}"
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

WORKDIR /build

COPY requirements.txt requirements-audio.txt ./

RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt \
    && if [ "${INSTALL_AUDIO}" = "true" ]; then \
         pip install -r requirements-audio.txt; \
       else \
         echo "Audio dependencies are skipped (INSTALL_AUDIO=${INSTALL_AUDIO})."; \
       fi


FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:${PATH}" \
    HF_HOME=/tmp/meet-core-cache/huggingface \
    TORCH_HOME=/tmp/meet-core-cache/torch

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        ffmpeg \
        libgomp1 \
        libsndfile1 \
    && rm -rf /var/lib/apt/lists/* \
    && addgroup --system meetcore \
    && adduser --system --ingroup meetcore --home /home/meetcore meetcore \
    && mkdir -p /app /tmp/meet-core-cache \
    && chown -R meetcore:meetcore /app /home/meetcore /tmp/meet-core-cache

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY --chown=meetcore:meetcore app ./app

USER meetcore

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
