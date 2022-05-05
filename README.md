# SENG3011 Project - Epidemic Eagle

## **Introduction**
Epidemic Eagle is an all-in-one solution. It provides a frontend solution for travel agencies as well as an API for news articles (currently not implemented).

### **Travel Agency Website**
The frontend website was our idea to validate the idea of the API. In our project, we decided to go with a travel agency website, which provides the ability to communicate with each other.
#### **Custom Features of the Website**
### Copy-Paste Button
> <p align="center"><img src=pics/1.png width="70%" /><img src=pics/2.png width="70%"/></p>
### Using External API calls
> <p align="center"><img src=pics/3.png width="70%" /><img src=pics/4.png width="70%"/></p>

```
    def covid_api(dest):
    url = "https://disease.sh/v3/covid-19/countries/" + dest + "?strict=true"
    response = requests.get(url)
    return response.json()
```

```
def risk_level(location):
    f = open("country_codes.json", 'r')
    data = json.load(f)
    code = data.get(location, "not found")
    if code == 'not found':
        return "No risk data detected."
    else:
        response = requests.get('https://www.travel-advisory.info/api')
        a = response.json()['data'][code]['advisory']
    return a
```

## **API**
For this project, we had to create an API for searching news articles and returning the information into a JSON format. In our case it was ProMed. This was not completed in time.


# **Documentation**
## **Phase 1**
To run phase1, run these two commands:
```
./setup.sh
./phase1.sh
```
## View API Documentation
```
http://localhost:8000/docs
```
<br>

## **Phase 2**
To run phase2, run these two commands:
```
./setup.sh
./phase2.sh
```
## View API Documentation
```
http://localhost:8000/docs
```
