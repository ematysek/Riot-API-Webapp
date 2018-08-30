# Riot-API-Webapp

The goal of this project is to be a self hosted web application to lookup League of Legends Summoners and view statistics.  
Currently in early stages of development.  
Developed and tested using Python 3.6.5

## Getting Started

1. Git clone the project
2. Pip install the requirements  
```pip install -r requirements.txt```
3. Rename example.env to .env and provide API_KEY.  
Anything in .env or .flaskenv can also be provided by environmental variables.  
Currently the defaults in these files are for development and should not be used in "production"
4. Initialize and bring the db to the latest schema  
```flask db upgrade```
5. Run the application  
```flask run```

## Goals / TODO

- Testing
- Fill out the front end
- Generate interesting statistics
- API rate limiting
- Implement gunicorn and run behind NGINX