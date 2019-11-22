FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add --virtual build-deps gcc python3-dev musl-dev jpeg-dev zlib-dev

WORKDIR /app
COPY . /app/
RUN chmod 777 *
RUN ls -la
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["/app/start.sh"]
