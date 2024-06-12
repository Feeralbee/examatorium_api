FROM python:3.11-bookworm
WORKDIR /app

RUN apt-get update
RUN apt-get install python3-dev -y
RUN apt-get install libpq-dev gcc -y
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

CMD [ "uvicorn", "--factory", "application.main:main", "--host=0.0.0.0"]
