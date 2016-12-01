# tweetanalyser
Werkstuk programma voor ISCP


## Instalatie
Installeer alle packages die worden gebruikt
```sh
install requirements.txt
```
Voeg je twitter.api sleutels toe aan settings.py

```sh
CONSUMER_KEY = 	''
CONSUMER_SECRET = ''

ACCESS_TOKEN = ''
ACCESS_SECRET = ''
```
Zet de database op
```sh
python manage.py migrate
python manage.py makemigrations tweets
python manage.py migrate
python manage.py createsuperuser
```
Alles is nu gereed, en we kunnen nu de applicatie opstarten
```sh
python manage.py runserver
```

## Toegangkelijkheid
De server staat aan en is beschikbaar op de localhost port 8000 :
127.0.0.1:8000
