FROM python:3.9
WORKDIR /app
COPY requrements.txt ./
RUN pip install -r requrements.txt
ADD ./webserver/api.py ./

CMD ["python", "api.py"]
