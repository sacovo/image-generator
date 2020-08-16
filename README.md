# Image Generator
Tool to add text to user uploaded images.

## Usage
Setup the templates and upload the neccesary fonts in the django admin. Each template can have multiple text overlays and image overlays. The text overlays are displayed to the end useres with a text input. Additionally you can allow users to change the font size, the font color or the background color.

Example here: https://so-me.juso.ch/

## Setup

Clone repository

```
docker-compose up -d 
```

## Deployment

```
docker-compose -f docker-compose.prod.yml up -d
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```


For production copy .env.dev to .env.prod and change passwords and keys.
Change trafik labels to fit domain.

## Structure
Configuration is in the top-directory: `settings.py`, `urls.py`

docker-compose.prod.yml is prepared for use with the traefik load balancer.


