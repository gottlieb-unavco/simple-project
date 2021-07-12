FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /django
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . ./
RUN python manage.py migrate
