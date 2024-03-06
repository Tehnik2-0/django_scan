FROM python:3.12
ENV PYTHONUNBUFFERED 1
RUN mkdir /djangoProject
WORKDIR /djangoProject
COPY requirements.txt /djangoProject/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /djangoProject/