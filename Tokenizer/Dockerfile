FROM python:3.10-slim

RUN apt-get update
RUN python -m ensurepip && \
    python -m pip install --upgrade pip==24.0
RUN pip install poetry==1.8.2

WORKDIR /app

#COPY pyproject.toml poetry.lock README.md ./
COPY pyproject.toml README.md ./
COPY . .

RUN poetry config virtualenvs.create false
RUN poetry install --without dev

EXPOSE 5001

CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]
