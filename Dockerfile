FROM python:3

WORKDIR /usr/src/app

ENV DB_DRIVER=mysql+pymysql
ENV DB_HOST=db
ENV DB_PORT=3306
ENV DB_NAME=testdb
ENV DB_USER=testuser
ENV DB_PASS=testp@ss
ENV RABBIT_HOST=db
ENV RABBIT_QUEUE=hello
ENV LOG_LEVEL=WARNING

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN ["alembic", "upgrade", "head"]
CMD ["python", "worker/main.py"]