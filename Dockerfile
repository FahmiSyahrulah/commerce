FROM python:3.6.7
MAINTAINER syahrulah "fahmi@alphatech.id"
RUN mkdir -p /demo
COPY . /demo
RUN pip install -r /demo/requirements.txt
WORKDIR /demo
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
