FROM python:3.8-bullseye
WORKDIR /app/skripsi
COPY . /app/skripsi
RUN pip install -r requirements.txt
EXPOSE 3000
CMD python app.py
