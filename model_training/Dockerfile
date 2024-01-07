FROM python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock ./

ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install --no-cache-dir poetry==1.7.1 \
        && poetry install --no-root

COPY model_training /opt/ml/code/model_training
COPY train.py /opt/ml/code/train.py

ENV SAGEMAKER_PROGRAM train.py