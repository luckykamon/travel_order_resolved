FROM ubuntu:20.04
ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update
RUN apt-get install python3-pip ffmpeg -y
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8989
RUN python3 -c "import nltk;nltk.download('all')"
ENTRYPOINT [ "python3" ]
CMD [ "nlp_perso.py" ]