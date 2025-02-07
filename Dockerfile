FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

COPY . /app

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN apt-get update && apt-get install -y supervisor 

RUN apt-get update && apt-get install -y \
    libsqlite3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y ffmpeg

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 4376 5672 15672

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
