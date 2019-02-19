FROM alpine

MAINTAINER IV8<admin@30m.cloud>

ENV UID=uid\
 UPWD=upwd\
 SMIN=300\
 SMAX=600

COPY run.py /root/hostloc/run.py

RUN apk --no-cache add python &&\
 apk --no-cache add --virtual .build-deps py-pip &&\
 pip install --upgrade pip &&  pip install requests BeautifulSoup beautifulsoup4 &&\
 apk del .build-deps && rm -rf ~/.cache /tmp

WORKDIR /root/hostloc

CMD sed -i "s|useruid|$UID|" /root/hostloc/run.py &&\
 sed -i "s|userpwd|$UPWD|" /root/hostloc/run.py &&\
 sed -i "s|time1|$SMIN|" /root/hostloc/run.py &&\
 sed -i "s|time2|$SMAX|" /root/hostloc/run.py &&\
 python -u /root/hostloc/run.py
