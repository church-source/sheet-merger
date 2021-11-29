# sheet-merger

###To run locally:

```
git clone https://github.com/church-source/sheet-merger
cd sheet-merger
virtualenv venv
source venv/bin/activate
cd src
pip install -r requirements.txt
python -m run 
```

###Using Docker
Build with docker: 
```
git clone https://github.com/churchsource/sheet-merger
cd sheet-merger/src
docker build -t sheet-merger .
```

Run in development mode: 
```
docker run -dt --name=sheet-merger -v $PWD:/app -p 5000:5000 -e 'WORK_ENV=DEV' sheet-merger
```

Run in production mode:
```
docker run -dt --restart=always --name=sheet-merger -p 5000:5000 -e 'WORK_ENV=PROD' sheet-merger
```

Remove the container:
```
docker rm -f sheet-merger
```

To see logs and connect the container:
```
docker logs --follow sheet-merger
docker exec -it sheet-merger bash

```