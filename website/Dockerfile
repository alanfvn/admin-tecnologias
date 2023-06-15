FROM python:3.9-alpine

WORKDIR /app
COPY req.txt .
RUN pip install -r req.txt
COPY src ./src

CMD python src/manage.py runserver 0.0.0.0:8000
