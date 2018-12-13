FROM python:3-slim-stretch AS image-builder
WORKDIR /usr/src/app
COPY requirements.txt ./

RUN pip install -U pip \
        && pip wheel -r ./requirements.txt
COPY . .

FROM gcr.io/distroless/python3
COPY --from=image-builder /usr/src/app /app

RUN pip install -U pip \
       && pip install -r /app/requirements.txt \
                      -f /app \
WORKDIR /app
CMD [ "./server.py" ]
