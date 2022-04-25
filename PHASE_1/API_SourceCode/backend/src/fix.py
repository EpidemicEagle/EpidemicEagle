import json
s = [
        {
          "destination": "Bangkok, Thailand",
          "email": "stanleyparks@gmail.com",
          "location": "Sydney, Australia",
          "name": "Stanley Parks",
          "phone": "083 555 6733"
        },
        {
          "destination": "Swansea, Wales",
          "email": "ewright@gmail.com",
          "location": "Birmingham, England",
          "name": "Edgar Wright",
          "phone": "074 555 1491"
        },
        {
          "destination": "Washington, USA",
          "email": "mdsouza@gmail.com",
          "location": "Toronto, Canada",
          "name": "Maria de Souza",
          "phone": "073 555 3921"
        },
        {
          "destination": "Durban, South Africa",
          "email": "jjones@gmail.com",
          "location": "Manchester, England",
          "name": "Jon Jones",
          "phone": "084 555 4143"
        },
        {
          "destination": "Windhoek, Namibia",
          "email": "sjakes@gmail.com",
          "location": "Cape Town, South Africa",
          "name": "Sibusiso Jacob",
          "phone": "074 555 8127"
        }
      ]
    # 
    #   "agency": 1,
    #   "destination": "Bangkok, Thailand",
    #   "email": "stanleyparks@gmail.com",
    #   "end_date": "2022-10-10",
    #   "start_date": "2020-01-01",    
    #   "location": "Sydney, Australia",
    #   "name": "Stanley Parks",
    #   "password": "abc123",
    #   "phone": "0999999999",

    #   "u_id": 1
    # },


for i in s:
    i['end_date'] = "2022-10-10"
    i["start_date"] = "2020-01-01"
    i["password"] = "abc123"
print(json.dumps(s))