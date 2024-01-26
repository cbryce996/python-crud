FROM python:3.8

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y nodejs npm

RUN npm install
RUN npm run build

EXPOSE 5000

ENV NAME World

CMD ["python", "app.py"]