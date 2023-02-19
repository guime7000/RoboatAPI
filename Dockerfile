FROM python:3.9-bullseye

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

ENTRYPOINT ["./entrypoint.sh"]
CMD ["server"]
