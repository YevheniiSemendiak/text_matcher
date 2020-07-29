import json
import os
import time
import logging

import pika

import text_matcher as tm
from utils import MongoDBDAO

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-5s - %(name)s:%(lineno)d |> %(message)s",
    datefmt="%d.%m.%Y %H:%M:%S"
)


class API:
    def __init__(self):
        self.rmq_connection = pika.BlockingConnection(
            parameters=pika.ConnectionParameters(
                host=os.getenv("TEXT_MATCHER_RMQ_HOST"),
                port=int(os.getenv("TEXT_MATCHER_RMQ_AMQP_PORT"))
            )
        )
        self.db_dao = MongoDBDAO(
            mongo_host=os.getenv("TEXT_MATCHER_MONGO_ADDR"),
            mongo_port=int(os.getenv("TEXT_MATCHER_MONGO_PORT")),
            database_name=os.getenv("TEXT_MATCHER_MONGO_DB_NAME"),
            user=os.getenv("TEXT_MATCHER_MONGO_USER"),
            passwd=os.getenv("TEXT_MATCHER_MONGO_PASS")
        )
        self.text_matcher = tm.TextMatcher(self.db_dao)
        self.logger = logging.getLogger(__name__)

    # --------------
    # API messages handlers
    # -------------->
    def new_text(self,
                 channel: pika.channel.Channel,
                 method: pika.spec.Basic.Deliver,
                 properties: pika.spec.BasicProperties,
                 body: bytes):
        request = json.loads(body)
        response = {
            "success": False,
            "error": "",
            "textUUID": "",
            "type": "processText"
        }

        if self.wait_matcher_is_ready(5):
            try:
                response["textUUID"] = self.text_matcher.process_new_text(request)
                response["success"] = True

            except Exception as err:
                self.logger.error(err, exc_info=err)
                response["error"] = str(err)
        else:
            response["error"] = f"TextMatcher is not IDLE: {self.text_matcher.state}"

        channel.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            body=json.dumps(response),
            properties=pika.BasicProperties(
                correlation_id=properties.correlation_id,
                content_type="application/json"
            )
        )
        channel.basic_ack(delivery_tag=method.delivery_tag)
        channel.basic_publish(
            exchange="logs",
            routing_key="",
            body=json.dumps(
                {
                    "level": "info",
                    "type": "success",
                    "message": f"Successfully processed text (ID: {response['textUUID']})."
                }
            ),
            properties=pika.BasicProperties(
                content_type="application/json"
            )
        )

    def get_sentence_distances(self,
                               channel: pika.channel.Channel,
                               method: pika.spec.Basic.Deliver,
                               properties: pika.spec.BasicProperties,
                               body: bytes):
        response = {
            "success": False,
            "error": "",
            "type": "SentenceDistances",
            "distances": []  # key-values: { "distance": np.float "metric": str "_id": str }
        }
        request = json.loads(body)

        try:
            if self.wait_matcher_is_ready(5):
                response["distances"] = self.text_matcher.get_sorted_distances(request["sentenceUUID"])
                response["success"] = True
        except Exception as err:
            self.logger.error(err, exc_info=err)
            response["error"] = str(err)

        channel.basic_publish(
            exchange='' if properties.reply_to else "logs",
            routing_key=properties.reply_to or "",
            body=json.dumps(response),
            properties=pika.BasicProperties(
                correlation_id=properties.correlation_id,
                content_type="application/json"
            )
        )
        channel.basic_ack(delivery_tag=method.delivery_tag)

    # --------------
    #  Helper methods
    # -------------->
    def wait_matcher_is_ready(self, timeout: int = None) -> bool:
        started = time.time()
        while self.text_matcher.state != tm.IDLE and time.time() - started < timeout:
            time.sleep(0.1)
        assert self.text_matcher.state == tm.IDLE, "Text matcher is not ready."
        return True

    def run(self):
        """
        Point of entry to the server part of PRC,
        listening of queues with PRC requests
        """
        rmq_channel = self.rmq_connection.channel()
        rmq_channel.basic_qos(prefetch_count=1)

        rmq_channel.basic_consume(queue='front_to_back_text', on_message_callback=self.new_text)
        rmq_channel.basic_consume(queue='front_to_back_sentences', on_message_callback=self.get_sentence_distances)

        self.logger.info("Back-end is ready.")

        try:
            rmq_channel.start_consuming()
        except KeyboardInterrupt:
            rmq_channel.stop_consuming()
        finally:
            if self.rmq_connection.is_open:
                self.rmq_connection.close()


if __name__ == '__main__':
    api = API()
    api.run()
