FROM python:3.6.7-slim

RUN apt-get update && apt-get -y install netcat && apt-get clean

WORKDIR /app

COPY tasks ./tasks
COPY app.py .
COPY arithmetic.py .
COPY config.py .
COPY constants.py .
COPY schemas.py .
COPY views.py .
COPY web.py .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY run-web.sh .
RUN chmod +x run-web.sh

COPY run-worker.sh .
RUN chmod +x run-worker.sh

CMD ./run-worker.sh
