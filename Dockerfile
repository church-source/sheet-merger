FROM python:3.8-slim-buster
RUN apt-get update -y
RUN apt-get install -y git
# python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "run.py"]

# docker build -t church-telegram-bot-bff .
# 
# For Development Container
# docker run -dt --name=sheet-merger -v $PWD:/app -p 5000:5000 -e 'WORK_ENV=DEV' sheet-merger
# 
# For Production Container
# docker run -dt --restart=always --name=sheet-merger -p 5000:5000 -e 'WORK_ENV=PROD' sheet-merger
# 
# Remove the container
# docker rm -f sheet-merger

# docker logs --follow sheet-merger
# docker exec -it sheet-merger bash
