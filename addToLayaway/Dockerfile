FROM python:3.8.8-alpine
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
EXPOSE 5002
CMD ["python", "app.py"]