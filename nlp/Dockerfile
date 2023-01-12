FROM ubuntu:20.04
ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update
RUN apt-get install python3-pip ffmpeg -y
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8989
RUN python3 -c "import nltk;nltk.download('stopwords');nltk.download('punkt')"
ENTRYPOINT [ "python3" ]
CMD [ "nlp_perso.py" ]