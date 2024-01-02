FROM python:3.11-slim

ADD . .
RUN pip freeze > requirements.txt
RUN pip install -r  requirements.txt


CMD python main.py