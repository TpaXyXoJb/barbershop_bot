FROM python:3.12

RUN pip install poetry

WORKDIR /app

COPY . /app

RUN poetry install --no-root

CMD ["poetry", "run", "python", "bot/main.py"]
