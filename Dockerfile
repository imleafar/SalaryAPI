FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /salaryAPI

WORKDIR /salaryAPI

ADD . /salaryAPI/

RUN pip install -r requirements.txt