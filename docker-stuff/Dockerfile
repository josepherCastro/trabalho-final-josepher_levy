  
FROM python:3-alpine

LABEL mantainer="Josepher Castro,Levy Ferreira"

# install system-wide deps for python and node

RUN apk update && \
    apk upgrade && \
    apk add git
# expose port
EXPOSE 5000
RUN git clone https://github.com/ppdtads2019/trabalho-final-josepher_levy.git

CMD ["ifconfig"]
# start app
CMD [ "python", "./trabalho-final-josepher_levy/servidor/servidor.py" ]