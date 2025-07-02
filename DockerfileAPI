FROM python:3.12-slim-bookworm

WORKDIR /var/opt/

RUN useradd -ms /bin/sh -b /var/opt/ app && usermod -aG app app
USER app

ADD src ./app/src
ADD api ./app/api
COPY main.py ./app


COPY requirements.txt ./
RUN pip3 install -r ./requirements.txt

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["/var/opt/app/main.py"]