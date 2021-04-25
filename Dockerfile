FROM python:3.7-slim AS application

RUN set -ex; \
    apt-get update; \
    apt-get install --no-install-recommends -y \
        gcc \
        python3-dev \
        python3-pip \
        libxml2-dev \
        libxslt1-dev \
        zlib1g-dev g++ \
    ; \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

ENV REDIS_HOST=localhost
COPY . /usr/src/app
ENTRYPOINT ["python"]
CMD ["hashes/run.py"]
