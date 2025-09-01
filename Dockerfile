FROM python:3.10-alpine3.13
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ip.py favicon.ico ./
CMD python -u ip.py