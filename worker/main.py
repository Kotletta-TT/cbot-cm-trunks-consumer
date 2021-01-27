import pika
import sys
import os
import json
import logging
from models import SimVats
from db_helper import Session

RABBIT_HOST = os.environ.get('RABBIT_HOST')
RABBIT_QUEUE = os.environ.get('RABBIT_QUEUE')
LOG_LEVEL = os.environ.get('LOG_LEVEL') if os.environ.get('LOG_LEVEL') is not None else 'WARNING'

"""# Нужна проверка на валидные номера отличать от служебных/специальных/некорректных"""
"""# Проверка на подключение к Rabbit"""
"""# Как то ускорить работу с БД (множественный коммит?)"""
"""# Перезапись в БД?, уточнить!"""
"""# Проверка на запись/перезапись в БД"""


session = Session()

logger = logging.getLogger('TRUNK-PRODUCER')  # создаем логгер приложения
logger.setLevel(LOG_LEVEL)
logger.propagate = False  # отключаем стрим сообщений в корневой логгер
console_handler = logging.StreamHandler()  # создаем объект Stream для вывода логов только на экран
logger.addHandler(console_handler)
formatter = logging.Formatter(fmt='%(levelname)s:[%(name)s]:%(message)s')
console_handler.setFormatter(formatter)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    channel = connection.channel()

    channel.queue_declare(queue=RABBIT_QUEUE)

    def callback(ch, method, properties, body):
        message = json.loads(body)
        logger.info(f'Take trank-message to send in DB contract: {message["contract"]} tel: {message["tn"]}')
        simobj = SimVats(provider=message['provider'], contract=message['contract'], trank_login=message['targetName'],
                         phone=message['tn'])
        session.add(simobj)
        session.commit()
        logger.debug(f'Record trunk-message to DB contract: {message["contract"]} tel: {message["tn"]}')
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='hello', on_message_callback=callback)  # , auto_ack=True)

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
