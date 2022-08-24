FROM python:slim-buster
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["streamlit","run"]
CMD ["app.py" ]
EXPOSE 8501
