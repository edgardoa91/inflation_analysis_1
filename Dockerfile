FROM python:3.9-slim as os-base
ENV PYTHONUNBUFFERED=true
ENV PYTHONDONTWRITEBYTECODE=true
RUN apt-get update
RUN apt-get install -y curl

FROM os-base as poetry-base

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="/root/.poetry/bin:$PATH"
RUN poetry config virtualenvs.create false
RUN apt-get remove -y curl

FROM poetry-base as app-base

ARG APPDIR=/app
WORKDIR $APPDIR
COPY . ./
COPY pyproject.toml ./pyproject.toml
RUN poetry install --no-dev

FROM app-base as main
CMD ["poetry", "run", "streamlit", "run", "src/app.py", "--server.port", "8080"]

