FROM python:3.9

RUN mkdir web_service

WORKDIR web_service

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

EXPOSE 8080

CMD [ "python", "main.py" ]