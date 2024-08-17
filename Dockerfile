FROM python:3.12

ENV PYTHONUNBUFFERED True

EXPOSE 8080
WORKDIR /app

COPY . ./

RUN pip install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "./scripts/main.py", "--server.port=8080", "--server.address=0.0.0.0"]