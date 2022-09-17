FROM python:3.8

RUN mkdir -p /usr/src/python3.8

WORKDIR /usr/src/python3.8

COPY ./requirements.txt /usr/src/python3.8/requirements.txt

RUN pip install -r ./requirements.txt

COPY . /usr/src/python3.8

RUN mkdir -p /usr/src/python3.8/db

CMD ["python", "app.py"]
