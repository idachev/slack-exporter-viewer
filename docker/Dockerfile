FROM python:3.8-alpine

RUN apk add --no-cache bash

RUN apk update \
    && apk add --no-cache --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache jpeg-dev zlib-dev libjpeg \
    && pip3 install Pillow \
    && apk del build-deps

RUN pip3 install click flask emoji markdown2

ENV SLACK_EXPORTER_DIR=/opt/slack-exporter

RUN mkdir -p ${SLACK_EXPORTER_DIR}

COPY ./target/src/ ${SLACK_EXPORTER_DIR}/
COPY ./target/slack-export-viewer ${SLACK_EXPORTER_DIR}/

RUN chmod +x ${SLACK_EXPORTER_DIR}/slack-export-viewer

WORKDIR ${SLACK_EXPORTER_DIR}

EXPOSE 5000

ENTRYPOINT ["python3", "/opt/slack-exporter/slack-export-viewer", \
 "-z", "/opt/slack-exporter/exported", \
 "-p", "5000", \
 "--ip", "0.0.0.0"]
