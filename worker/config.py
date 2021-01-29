import yaml


def conf_parser(filename):
    with open(filename, 'r') as f:
        return yaml.safe_load(f)


conf = conf_parser('worker/config.yaml')

RABBIT_HOST = conf['rabbitmq']['host']
RABBIT_PORT = conf['rabbitmq']['port']
RABBIT_QUEUE = conf['rabbitmq']['queue']
LOG_LEVEL = conf['log-level']
LOG_NAME = conf['log-name']

DB_DRIVER = conf['db']['driver']
DB_HOST = conf['db']['host']
DB_PORT = conf['db']['port']
DB_USER = conf['db']['user']
DB_PASS = conf['db']['pass']
DB_NAME = conf['db']['name']
