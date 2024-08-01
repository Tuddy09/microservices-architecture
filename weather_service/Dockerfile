FROM microskel

ADD . /opt/weather_service
WORKDIR /opt/weather_service

RUN pip install -r requirements.txt

CMD ["python", "weather_service.py"]
