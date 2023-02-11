FROM python:3.10.8-slim-bullseye

RUN pip install --upgrade pip

WORKDIR /auth
RUN mkdir /auth/tests
RUN groupadd -r auth && useradd -d /auth -r -g auth auth

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY .. .
RUN chown auth:auth -R /auth

USER auth
CMD alembic init alembic && python3 main.py