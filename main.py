from fastapi import FastAPI, Path, Query

app = FastAPI()

with open('database.txt', 'r') as file: #read -> r
    database = file.readlines()
    file.close()

database_dictionary={}

for i in range(len(database)): # convert the array into a dictionary to better sort the information for the api
    database[i] = database[i].replace('\n','')
    index_value_of_comma = database[i][2:].index(',') # the position of the second comma is acquired
    database_dictionary[database[i][0]]={'country':database[i][3:index_value_of_comma+2], 'city':database[i][index_value_of_comma+4:] }

#1 Que permita saber si el API está activo.
@app.get("/")
async def index():
    return {
        'status': 200,
        'description': 'active',
        'body': database_dictionary
    }

#2 Que permita obtener el país de una ciudad que se le pase, y si la ciudad no existe, debe devolver "La ciudad no existe".
@app.get("/countries") #get the names of all the countries
async def get_countries():
    countries = []    
    for i in database_dictionary:
        countries.append(database_dictionary[i]['country'])
    return {'countries':countries}

#3 Que permita obtener el país de una ciudad que se le pase, y si la ciudad no existe, debe devolver "La ciudad no existe".
@app.get("/getCountryByCity/{city_name}")
async def get_country_by_city(city_name: str = Path(None, description='get the country name by the city name')):
    for i in database_dictionary:
        if database_dictionary[i]['city'].lower() == city_name.lower() or database_dictionary[i]['city'].replace(' ','').lower() == city_name.lower():
            return database_dictionary[i]['country']
    return {
        'status':400,
        'description':'La ciudad no existe'
    }

#4 Que permita obtener el país y la ciudad cuando se pase un id, y si el id no existe, debe devolver "El id no existe".
@app.get("/id/{country_id}")
async def get_id(country_id: int = Path(None, description='The ID of the country you want to view'),gt='0'):
    country_id=str(country_id)
    if country_id not in database_dictionary.keys():
        return {
            'status':400,
            'description':'Country does not exist'
        }
    return  database_dictionary[country_id]

#5 Que permita agregar una nueva ciudad y país con un Request Parameter.
@app.delete('/delete-country/{country_id}')
async def delete_country(country_id: int = Path(None, description='The ID of the country you want to delete')):
    country_id=str(country_id)
    if country_id not in database_dictionary.keys():
        return {
            'status':400,
            'description':'Country does not exist'
        }
    del database_dictionary[country_id] 
    return {'message':'Country deleted successfully'}

#6 Que permita eliminar una ciudad y país, pasando su id con un Query Parameter
@app.post("/createCountry/{country_name}/{city_name}")
async def create_country(country_name:str = Path(None, description='add country name'), city_name: str = Path(None, description='add city name')):
    for i in database_dictionary:
        i=str(i)
        if database_dictionary[i]['country'].lower() == country_name.lower() or database_dictionary[i]['country'].replace(' ','').lower() == country_name.lower():
            return {
                'status':400,
                'description':'Country already exists'
            }
    index_value = str(int(list(database_dictionary)[-1])+1) # get latest id value from database
    database_dictionary[index_value]={'country': country_name, 'city': city_name}
    return database_dictionary