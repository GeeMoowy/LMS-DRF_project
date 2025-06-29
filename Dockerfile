FROM python:3.13

ENV POETRY_VERSION=1.8.5
RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
