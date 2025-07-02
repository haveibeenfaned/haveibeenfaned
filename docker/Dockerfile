FROM python:3.12-slim-bookworm

COPY src .
COPY requirements.txt .
RUN apt update -y && apt upgrade -y
RUN apt install -y libglib2.0-0 \
 libnss3 \
 libgconf-2-4 \
 libfontconfig1

RUN pip3 install -r ./requirements.txt

CMD ["python3"]