# Following the best practice
# Is better to specify the version used
FROM python:3.12.9-slim
MAINTAINER Luigi Maffiola
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1

WORKDIR /app/

# Installing dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project
# Installing uv
COPY --from=ghcr.io/astral-sh/uv:0.6.2 /uv /uvx /bin/

RUN apt-get update -y
RUN apt-get install iputils-ping -y
COPY ./src /app/src
COPY ./static /app/static
COPY ./templates /app/templates
COPY ./pyproject.toml ./uv.lock /app/
#COPY ./tests /mirai_api/tests
#COPY ./scripts /mirai_api/scripts
#COPY ./alembic.ini /mirai_api/alembic.ini
#COPY ./alembic /mirai_api/alembic
# Expose ports are used for informative purpose
# These are the ports intended to be published with -p
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

EXPOSE 5432
CMD ["python", "-m", "app.main"]
