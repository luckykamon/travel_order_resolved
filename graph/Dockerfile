FROM ubuntu:20.04
ENV TZ=Europe/Paris
EXPOSE 8000
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update
RUN apt-get install python3-pip flac -y
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install unidecode
RUN pip install xlrd
COPY . .
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
