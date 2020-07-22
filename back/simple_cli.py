import json
import logging

from utils import MongoDBDAO

import pika


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-8s - %(name)s:%(lineno)d |> %(message)s",
    datefmt="%d.%m.%Y %H:%M:%S"
)


STORAGE = []

mongo_dao = MongoDBDAO("localhost", 27017, "text_matcher", "admin", "securePasswd!")
conn = pika.BlockingConnection(parameters=pika.ConnectionParameters("localhost", 49153))
ch = conn.channel()
temp_queue = ch.queue_declare(queue='', exclusive=True)
temp_queue_name = temp_queue.method.queue


def on_reply(ch, method, properties, body):
    logging.info(f"Got an message in {method.routing_key} queue!")
    logging.info(body)
    global STORAGE
    STORAGE.append((method, properties, body))
    ch.basic_ack(delivery_tag=method.delivery_tag)


ch.basic_consume(temp_queue_name, on_message_callback=on_reply)


def send_text():
    with open("text.txt") as f:
        texts = f.readlines()
    logging.info("Available texts:")
    for i, t in enumerate(texts):
        logging.info(f"{i}: {t}")
    comm = input("Insert a valid number, or own text to send it.")
    try:
        tts = texts[int(comm)]
    except (ValueError, IndexError) as e:
        tts = comm
    ch.basic_publish(
        exchange="",
        routing_key="front_to_back_text",
        body=json.dumps({"text": tts, "title": f"{tts[:10]}..."}),
        properties=pika.BasicProperties(
            content_type="application/json"
        )
    )
    logging.info(f"Text '{tts[:10]} ... {tts[-10:]}' sent!")


def get():
    what = input("what you want to get (Sentence or Text): ")
    _id = input("_id (leave empty for all):")
    if not _id:
        logging.info(mongo_dao.get_records(what, None, None))
    else:
        logging.info(mongo_dao.get_records(what, {"_id": _id}, None))


def get_similarity():
    _id = input("_id:")
    ch.basic_publish(
        exchange="",
        routing_key="front_to_back_sentences",
        body=json.dumps({"sentenceUUID": _id}),
        properties=pika.BasicProperties(
            content_type="application/json",
            reply_to=temp_queue_name
        )
    )


def exit_():
    logging.info("Closing the connection.")
    ch.close()
    conn.close()
    while not conn.is_closed or not ch.is_closed():
        conn.process_data_events(0.5)


def check_new_messages():
    conn.process_data_events(0.5)


menu = {
    "1": {"description": "Fetching data from MongoDB.", "func": get},
    "2": {"description": "Search for similar sentence.", "func": get_similarity},
    "3": {"description": "Process and add new text to MongoDB.", "func": send_text},
    "4": {"description": "Check if new messages appeared.", "func": check_new_messages},
    "5": {"description": "Exit from CLI.", "func": exit}
}
while True:
    try:
        print("\n---- Menu ----")
        [print(f"{k} => {v['description']}") for k, v in menu.items()]
        menu[input("Enter function number:")]['func']()
    except Exception as e:
        logging.error(f"exception happened: {e}", exc_info=e)
        continue
