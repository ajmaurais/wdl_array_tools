from python:3.9-alpine

MAINTAINER "Aaron Maurais -- MacCoss Lab"

RUN apk add --no-cache bash xmlstarlet zip && \
    cd / && mkdir -p code/wdl_array_tools

ADD . /code/wdl_array_tools

RUN cd /code/wdl_array_tools && \
    pip install . && \
    python test/test_*.py

WORKDIR /data

CMD ["wdl_array_tools"]

