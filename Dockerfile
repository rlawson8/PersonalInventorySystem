FROM nginx:latest
LABEL maintainer="trevorj@sudocorpmail.com"
RUN apt-get -y update && apt-get -y upgrade && apt-get -y install python3.8
