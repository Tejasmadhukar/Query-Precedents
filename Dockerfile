FROM python:3.11-slim

WORKDIR /app

ADD . /app

RUN pip install pipenv 
RUN pipenv install --ignore-pipfile --system

EXPOSE 80

CMD ["python", "index.py"]