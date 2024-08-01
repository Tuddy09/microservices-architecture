FROM tuddy09/microskel24

ADD . /opt/events_service
WORKDIR /opt/events_service

RUN pip install -r requirements.txt

CMD ["python", "events_service.py"]
