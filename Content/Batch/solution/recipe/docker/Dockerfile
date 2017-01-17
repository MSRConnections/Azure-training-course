FROM ubuntu

MAINTAINER Blaize Stewart

ADD text2ogg.sh /text2ogg.sh
RUN apt-get update && \
	apt-get install -y espeak vorbis-tools && \
	chmod +x text2ogg.sh && \
	mkdir /fileshare
CMD ["sh" "text2ogg.sh"]