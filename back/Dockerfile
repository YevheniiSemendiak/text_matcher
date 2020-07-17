FROM pytorch/pytorch:latest

RUN apt-get update -qq && apt-get install -y -qq wget && apt-get clean

# Installing dockerize tool
ENV DOCKERIZE_VERSION v0.6.1

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

COPY requirements.txt /root
RUN pip install --no-cache-dir -q -r /root/requirements.txt
# Preloading BERT model (will be saved into cache)
RUN python -c 'from sentence_transformers import SentenceTransformer as ST; ST("bert-base-nli-mean-tokens")'

COPY . /root
WORKDIR /root

CMD dockerize -wait tcp://${TEXT_MATCHER_RMQ_HOST}:${TEXT_MATCHER_RMQ_AMQP_PORT} python -u api.py