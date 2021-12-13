FROM python:3.9
WORKDIR /app
COPY requrements.txt .
RUN pip install -r requrements.txt
COPY ./webserver/api.py .

ENTRYPOINT [ "python" ]
CMD [ "api.py" ]