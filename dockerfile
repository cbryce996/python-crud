FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN pytest

EXPOSE 5000

CMD ["python", "main.py"]