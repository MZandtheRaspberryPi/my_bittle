FROM python3.9:latest

COPY requirements-dev.txt /requirements-dev.txt
COPY requirements.txt /requirements.txt
RUN pip install -r requirements-dev.txt