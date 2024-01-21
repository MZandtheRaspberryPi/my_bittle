FROM python3.9:latest

COPY requirements.txt /requirements.txt
RUN pip install -r requirements-dev.txt