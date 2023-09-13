FROM python:3.8
LABEL maintainer="jdamerow@asu.edu"

RUN apt-get update
RUN apt install -y tesseract-ocr
RUN apt install -y libtesseract-dev
RUN apt install -y default-jre

WORKDIR stanford-ner
RUN wget https://nlp.stanford.edu/software/stanford-ner-4.2.0.zip && unzip stanford-ner-4.2.0.zip
WORKDIR /code
COPY extract.py .
COPY testimage.png .
COPY requirements.txt .
COPY prepare.py .

RUN pip install -r requirements.txt
RUN python prepare.py

CMD ["python", "extract.py", "testimage.png"]
