FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /coded
COPY requirements.txt /coded/
RUN pip install -r requirements.txt
COPY . /coded/
