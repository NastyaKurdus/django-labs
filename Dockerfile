FROM python:3.7
WORKDIR /api
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /api