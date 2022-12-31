FROM python:3.9


ENV DEBIAN_FRONTEND=noninteractive
RUN apt -qq update && apt -qq install -y ffmpeg

COPY . /app
WORKDIR /app
RUN chmod 777 /app

RUN pip3 install --no-cache-dir -r requirements.txt


CMD ["python3","-u","main.py"]