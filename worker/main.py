import time
import pika
import sys
import os
import json
from log_init import log_on
from models import Trunk
from db_helper import Session
from config import RABBIT_HOST, RABBIT_PORT, RABBIT_QUEUE, LOG_NAME

"""# Как то ускорить работу с БД (множественный коммит?)"""
"""# Перезапись в БД?, уточнить!"""
"""# Защита от падения/отсутствия коннекта с БД"""

session = Session()
logger = log_on(LOG_NAME)


def main():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST, port=RABBIT_PORT))
            logger.debug(f'Connect to RabbitMQ address: {RABBIT_HOST}')
            break
        except:
            logger.error(f'RabbitMQ CONNECTION ERROR: {RABBIT_HOST}')
            time.sleep(10)
            continue
    channel = connection.channel()
    channel.queue_declare(queue=RABBIT_QUEUE)

    def callback(ch, method, properties, body):
        message = json.loads(body)
        logger.info(f'Take trunk-message to send in DB object: {message["obj"]} phone: {message["phone"]}')
        trunk_obj = Trunk(*message)
        # query = session.query(Trunk).filter(Trunk.trunk_username == trunk_obj.trunk_username).first()
        # if query:
        session.add(trunk_obj)
        session.commit()
        logger.debug(f'Record trunk-message to DB object: {message["obj"]} phone: {message["phone"]}')
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=RABBIT_QUEUE, on_message_callback=callback)

    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
