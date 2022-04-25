import requests 



def Getting_poke_info(Pokemon):

    print("Getting pokemon Information...", end=' ')

#if nothing entered it will error out
    if Pokemon is None:
        print('error: Missing name parameter')
        return
#removes the white space surronding the pokemon name, if there is nothing afterwards it errors out.
    Pokemon == Pokemon.strip().lower()
    if Pokemon == "":
        print('error: empty parameter')
        return

#makes the http request to the pokeapi
    Response = requests.get("https://pokeapi.co/api/v2/pokemon/"+Pokemon)

    if Response.status_code == 200:
        print("SUCCESS")
        dict_response = Response.json() 
        return(dict_response)
    else:
        print("Response failed")
        return

def get_list(limit= 100, offset =0):

    url = "https://pokeapi.co/api/v2/pokemon/"

    params = {
        'limit'  : limit,
        'offset' : offset
    }

    resp_msg = requests.get(url,params=params)

#requests the data on all the pokemon that are with in the parameters specified(limit, offset)
    if resp_msg.status_code == 200:

        resp_dict = resp_msg.json()
    #returns just the names of the pokemon
        return [p['name'] for p in resp_dict['results']]

#prints the contents of the response message if it fails    
    else:
        print(resp_msg.text)

def pokemon_url(name):
#grabs the url of the pokemon image. returns non if it fails    
    poke_dict = Getting_poke_info(name)
    if poke_dict:
        return poke_dict['sprites']['other']['official-artwork']['front_default']
        