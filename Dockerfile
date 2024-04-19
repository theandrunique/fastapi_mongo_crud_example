FROM python:3

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY src src/

COPY logger_config.yml .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "logger_config.yml"]
