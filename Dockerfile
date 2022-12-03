FROM python:3.10-slim as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

RUN pip install pipenv

COPY ./Pipfile .
COPY ./Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base as runtime

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y python3-opencv

RUN useradd --create-home appuser
WORKDIR /home/appuser

COPY ./server .
COPY ./entrypoint.sh .
RUN chmod +x entrypoint.sh

USER appuser

EXPOSE 50051

ENTRYPOINT ["bash", "entrypoint.sh"]