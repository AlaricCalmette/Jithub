FROM python:3-slim-stretch
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt && rm -rf /root/.cache
COPY *.py Procfile *.json *.pem /app/
CMD [ "python", "server.py" ]
