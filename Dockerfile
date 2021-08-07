FROM python:3.8-buster

ENV PYTHONUNBUFFERED 1

COPY ./app /app

EXPOSE 5000

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]