FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FAKER_SERVER_PORT 3000

# Install pip requirements
ADD requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
ADD . /app

RUN useradd user && chown -R user /app
USER user

EXPOSE ${FAKER_SERVER_PORT}

CMD ["python", "faker_server/__main__.py"]
