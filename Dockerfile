FROM alpine:3.12

RUN apk update && \
    apk add bash python3 py3-pip && \
    pip3 install --upgrade pip

RUN pip3 install jinja2 rich typer

RUN apk add docker docker-compose

COPY app /app

ENV PATH="${PATH}:/app" \
    TERM="xterm-256color"

RUN playwithansible --install-completion bash
    