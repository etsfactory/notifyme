FROM python:3
ADD notify_me.py /
RUN pip3 install -r requirements.txt
CMD [ "python3", "./notify_me.py" ]