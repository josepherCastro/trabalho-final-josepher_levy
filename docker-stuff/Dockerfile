  
FROM python:3-alpine

LABEL mantainer="Josepher Castro,Levy Ferreira"

# install system-wide deps for python and node
RUN apk update


# expose port
EXPOSE 5000
RUN git clone https://github.com/ppdtads2019/trabalho-final-josepher_levy.git
CMD ["cd","servidor"]

# start app
CMD [ "python", "./servidor.py" ]