
FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./app/

RUN pip install -r /app/requirements.txt

EXPOSE 8080

CMD ["streamlit", "run" ,"./scripts/main.py", "--server.port", "8080"]