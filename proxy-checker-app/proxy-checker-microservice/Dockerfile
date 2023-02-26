FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
Run pip install psycopg2-binary 

COPY * .

EXPOSE 5001

CMD [ "python", "-u", "app.py" ]

