FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code

ENV DEBUG "False"
ENV DATABSE_URL "postgres://postgres:postgres@postgres:5432/postgres"
ENV SECRET_KEY "set_me_to_something_in_production"
ENV HOSTNAME "*"
ENV SENTRY_DSN ""
ENV MAILGUN_API_KEY ""

RUN pip install gunicorn
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN mkdir static
RUN python manage.py collectstatic --noinput

CMD [ "gunicorn", "server.wsgi:application", "--access-logfile", "-", "--error-logfile", "-" ]