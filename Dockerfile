FROM python:3.10-slim

WORKDIR /app

ARG ENVIRONMENT \
ARG ACCESS_KEY \
ARG SECRET_KEY

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ENVIRONMENT=$ENVIRONMENT \
    ACCESS_KEY=$ACCESS_KEY \
    SECRET_KEY=$SECRET_KEY \
    DJANGO_SETTINGS_MODULE=config.settings.$ENVIRONMENT

COPY . /app

RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-w", "3", "-k", "gevent", "config.wsgi:application"]