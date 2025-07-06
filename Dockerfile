# Will use this argument eventually to specify the python version so we can test against multiple versions
ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-slim-bookworm

ENV PATH="/root/.local/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install curl
RUN apt-get update -y && apt-get install -y \
    curl \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Install UV
ARG UV_VERSION=0.7.19
RUN curl -LsSf https://astral.sh/uv/${UV_VERSION}/install.sh | sh

WORKDIR /jsnac

# Copy relevant files only (using .dockerignore) then install our project as a package
COPY . .
RUN uv sync --locked

CMD ["/bin/bash"]