FROM python:3.8-slim
COPY requirements.txt /
RUN pip3 install -r /requirements.txt
RUN pip3 install gunicorn[gevent]
COPY . /app
WORKDIR /app
EXPOSE 5000
CMD gunicorn "app:create_app()" -w 2 --threads 2 -b 0.0.0.0:5000