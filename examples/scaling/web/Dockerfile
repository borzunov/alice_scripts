FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD gunicorn guess_number:skill --config gunicorn.conf.py

EXPOSE 80
