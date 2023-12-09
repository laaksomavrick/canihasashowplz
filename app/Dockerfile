FROM public.ecr.aws/lambda/python:3.11

COPY pyproject.toml src/canihaveatvshowplz/app.py ./

ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install --no-cache-dir poetry==1.1.11 \
        && poetry install --no-root

CMD ["app.lambda_handler"]
