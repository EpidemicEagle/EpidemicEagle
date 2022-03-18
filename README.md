# EpidemicEagle

# SETUP
```
pip install -r requirements.txt
```

# PHASE_1
## Backend Localhosting
```
./phase1.sh
```
## Swagger
http://127.0.0.1:8000/docs

## Testing
```
python -m pytest
```
## Logs
logs are currently generated using
```
heroku logs -n 200 app=epidemic-eagle > PHASE_1/TestScripts/logs
```