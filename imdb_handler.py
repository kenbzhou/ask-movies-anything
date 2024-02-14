import requests

def get_imdb_data_by_title(title):
    data = {}
    url = "https://imdb146.p.rapidapi.com/v1/find/"
    headers = {
        "X-RapidAPI-Key": "a0963f32d9msh4036904642d3c27p126865jsn91696e27ad67",
        "X-RapidAPI-Host": "imdb146.p.rapidapi.com"
    }
    queryString = {"query":title}
    response = requests.get(url, headers=headers, params=queryString)
    info = response.json()
    try:
        first_match = info['titleResults']['results'][0]
        data = get_imdb_data_by_id(first_match['id'])
    except:
        data = {"Error": "No movie or show by this title found"}
        
    return data

def get_imdb_data_by_id(id):
    url = "https://imdb146.p.rapidapi.com/v1/title/"
    querystring = {"id":id}
    headers = {
        "X-RapidAPI-Key": "a0963f32d9msh4036904642d3c27p126865jsn91696e27ad67",
        "X-RapidAPI-Host": "imdb146.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    info = response.json()
    data = {
        "title": info['titleText']['text'],
        "maturity-level": info['certificate']['rating'],
        "release-year": info['releaseDate']['year'],
        "plot": info['plot']['plotText']['plainText'],
        "rating": info['ratingsSummary']['aggregateRating'],
        "cast": [entry['node']['name']['nameText']['text'] for entry in info['cast']['edges']],
        "characters": [entry['node']['characters'][0]['name'] for entry in info['cast']['edges']]
    }

    return data

def get_entry_from_data(data, type):
    return data[type]

#a = get_entry_from_data(get_imdb_data_by_title("Rebel Moon"), "characters")
#print(a)