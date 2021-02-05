from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from config.conf import DB_DRIVER, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
# Есть косяк, для создания/применения миграции необходимо перед config ставить точку

url = URL(drivername=DB_DRIVER, username=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, database=DB_NAME,
          query={"charset": "utf8mb4"})

engine = create_engine(url, echo=True)

Session = sessionmaker(bind=engine)