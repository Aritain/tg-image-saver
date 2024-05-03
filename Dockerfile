FROM python:3.11.1-alpine3.17

COPY source/ /opt/tg_image_saver

RUN pip install -U pip
RUN pip install -r /opt/tg_image_saver/requirements.txt

WORKDIR /opt/tg_image_saver
ENTRYPOINT ["python3", "./main.py"]
