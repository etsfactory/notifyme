# this is an official Python runtime, used as the parent image
FROM python:3

# set the working directory in the container to /app
WORKDIR /app

# add the current directory to the container as /app
ADD . /app

# execute everyone's favorite pip command, pip install -r
RUN pip install -r requirements.txt

# unblock port 80 for the Flask app to run on
EXPOSE 5000

# execute the Flask app
CMD ["python", "./notify_me.py"]

# To run build the docker image:
# docker build . -t notifyme

# To run the docker image (runs without database, to use database use docker compose)
#docker run -p 5000:80 notifyme
