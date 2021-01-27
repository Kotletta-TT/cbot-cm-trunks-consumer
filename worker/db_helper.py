from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import os
from sqlalchemy.orm import sessionmaker

"""# Все ENVы в отдельный файл?"""

DB_DRIVER = os.environ.get('DB_DRIVER')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')

url = URL(drivername=DB_DRIVER, username=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, database=DB_NAME,
          query={"charset": "utf8mb4"})
engine = create_engine(url, echo=True)


Session = sessionmaker(bind=engine)

