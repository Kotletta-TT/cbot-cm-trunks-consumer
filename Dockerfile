FROM python:3

WORKDIR /usr/src/app


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN ["alembic", "upgrade", "head"]
CMD ["python", "./main.py"]