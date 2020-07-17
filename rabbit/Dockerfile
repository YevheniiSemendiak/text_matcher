FROM rabbitmq:3.8.5-management-alpine

RUN rabbitmq-plugins enable rabbitmq_web_stomp

COPY ./definitions.json /etc/rabbitmq/
COPY ./rabbitmq.config /etc/rabbitmq/
ENV RABBITMQ_LOGS=/var/log/rabbitmq/warning_log.log
# AMQP, Management GUI, STOMP
EXPOSE 49153 49154 49155
