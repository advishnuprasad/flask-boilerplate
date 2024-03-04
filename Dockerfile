FROM python:3.10

RUN mkdir /code
WORKDIR /code

COPY requirements.txt setup.py ./
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install -e .
RUN pip install gunicorn

COPY app myapp/
COPY migrations migrations/

WORKDIR /code/app

CMD ["gunicorn", "--conf", "gunicorn.py", "--bind", "0.0.0.0:3000", "wsgi:application"]