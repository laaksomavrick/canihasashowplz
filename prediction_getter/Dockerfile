FROM public.ecr.aws/lambda/python:3.11

COPY pyproject.toml poetry.lock ./

ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install --no-cache-dir poetry==1.7.1 \
        && poetry install --no-root

COPY prediction_getter prediction_getter

CMD ["prediction_getter/prediction_getter.lambda_handler"]
