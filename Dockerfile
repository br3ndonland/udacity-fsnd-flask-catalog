FROM python:alpine

LABEL Name=udacity-fsnd-p4-flask-catalog Version=0.2.0
EXPOSE 80
ENV APP_PORT 80
ENV APP_HOST '0.0.0.0'
ENV USER_NAME 'Brendon Smith'
ENV USER_EMAIL 'brendon.w.smith@gmail.com'
WORKDIR /app
ADD . /app

RUN python3 -m pip install -r requirements.txt
RUN python3 database_setup.py
RUN python3 database_data.py
CMD ["python3", "application.py"]
