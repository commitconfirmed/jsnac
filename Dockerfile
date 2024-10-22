# Will use this argument eventually to specify the python version so we can test against multiple versions
ARG PYTHON=3.11
FROM python:${PYTHON}-slim-bookworm

ENV PATH="/root/.local/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -yq curl \
    && curl -sSL https://install.python-poetry.org | python3 - --version 1.8.3 \
    && poetry config virtualenvs.create false

COPY pyproject.toml .
COPY poetry.lock .

# Dependencies change more often, so we break this out so the prevous apt-get is cached
RUN poetry install --no-interaction

ARG NAME=jsnac
WORKDIR /${NAME}

# Copy relevant files only (using .dockerignore) then install our project as a package
COPY . .
RUN poetry install --no-interaction

CMD ["/bin/bash"]