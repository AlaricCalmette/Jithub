FROM python:3-slim-stretch AS image-builder
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

FROM gcr.io/distroless/python3
COPY --from=image-builder /usr/src/app /app
WORKDIR /app
CMD [ "python", "./server.py" ]
