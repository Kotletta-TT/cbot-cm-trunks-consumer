import time
import pika
import sys
import os
import json
from app.log_init import log_on
from models.models import Trunk
from db.db_helper import Session
from config.conf import RABBIT_HOST, RABBIT_PORT, RABBIT_QUEUE, LOG_NAME

"""# Как то ускорить работу с БД (множественный коммит?)"""
"""# Защита от падения/отсутствия коннекта с БД"""

session = Session()
logger = log_on(LOG_NAME)


def init_read_db():
    db = {}
    temp_list = session.query(Trunk).all()
    if len(temp_list) > 1:
        for row in temp_list:
            key = f'{row.trunk_username}_{row.phone}'
            db[key] = row
    return db


def main():
    temp_db = init_read_db()
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
        key = f'{message["trunk_username"]}_{message["phone"]}'
        value = Trunk(**message)
        if key in temp_db:
            temp_db[key].obj = value.obj if temp_db[key].obj != value.obj else temp_db[key].obj
            temp_db[key].trunk_password = value.trunk_password if temp_db[key].trunk_password != value.trunk_password else temp_db[key].trunk_password
            temp_db[key].active = value.active if temp_db[key].active != value.active else temp_db[key].active
            temp_db[key].attributes = value.attributes if temp_db[key].attributes != value.attributes else temp_db[key].attributes
            temp_db[key].lines = value.lines if temp_db[key].lines != value.lines else temp_db[key].lines
            temp_db[key].updated = value.updated if temp_db[key].updated != value.updated else temp_db[key].updated
        else:
            temp_db[key] = value
        session.add(temp_db[key])
        session.commit()
        logger.debug(f'Record trunk-message to DB object: {message["obj"]} phone: {message["phone"]}')
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=RABBIT_QUEUE, on_message_callback=callback)

    channel.start_consuming()


def app_run():
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
