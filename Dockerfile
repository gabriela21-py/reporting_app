FROM python:3.12.2-bullseye

LABEL DESCRIPTION="Reporting application"

WORKDIR /usr/echipa3
COPY . .

RUN set -ex && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD flask run --host=0.0.0.0 --port=8000
