FROM python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock ./

ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install --no-cache-dir poetry==1.7.1 \
        && poetry install --no-root

COPY model_inference model_inference
COPY app.py app.py

ENV SM_MODEL_DIR /opt/ml/model

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8080", "app:app", "-n"]