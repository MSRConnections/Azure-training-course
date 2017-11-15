FROM ubuntu

MAINTAINER Blaize Stewart
COPY . /
RUN apt-get update && \
	apt-get install -y curl espeak vorbis-tools && \
	curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
	apt-get install -y nodejs && \
	npm install
	
WORKDIR /
CMD node /index.js