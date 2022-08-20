FROM python:3.7

WORKDIR . ./app

COPY . ./

COPY ./main.py ./

RUN pip install --upgrade pip

RUN pip install numpy numpy-financial

CMD ["python", "main.py"]