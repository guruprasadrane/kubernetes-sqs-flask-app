FROM python:3.11.0a7-alpine3.15

COPY . /opt

WORKDIR /opt

RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "web.py"]
