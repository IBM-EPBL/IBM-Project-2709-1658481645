FROM python:3.10.5
WORKDIR /app
ADD . /app
COPY . .
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install ibm_db
CMD ["python","app.py","-h","0.0.0.0"]
EXPOSE 5000
