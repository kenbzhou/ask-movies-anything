import requests
def get_data_by_title(title):
    data = {}
    headers = {
        "X-RapidAPI-Key": "a0963f32d9msh4036904642d3c27p126865jsn91696e27ad67",
        "X-RapidAPI-Host": "imdb146.p.rapidapi.com"
    }
    url_find = "https://imdb146.p.rapidapi.com/v1/find/"
    url_title = "https://imdb146.p.rapidapi.com/v1/title/"
    response = requests.get(url_find, headers=headers, params={"query":title})
    nfo = response.json()
    try:
        first_match = nfo['titleResults']['results'][0]
        response_title = requests.get(url_title, headers=headers, params={"id":first_match['id']})
        info = response_title.json()
        data = {
            "title": info['titleText']['text'],
            "maturity-level": info['certificate']['rating'],
            "release-year": info['releaseDate']['year'],
            "plot": info['plot']['plotText']['plainText'],
            "rating": info['ratingsSummary']['aggregateRating'],
            "cast": [entry['node']['name']['nameText']['text'] for entry in info['cast']['edges']],
            "characters": [entry['node']['characters'][0]['name'] for entry in info['cast']['edges']]
        }
    except:
        return f"Failed to retrieve data for {title}. Title might be incorrect"
        
    return data

def get_maturity_level(title):
    try: 
        data = get_data_by_title(title)
        return data['maturity-level']
    except:
        return f"Failed to retrieve maturity for {title}. Title might be incorrect"

def get_release_year(title):
    try: 
        data = get_data_by_title(title)
        return data['release-year']
    except:
        return f"Failed to retrieve release year for {title}. Title might be incorrect"

def get_plot(title):
    try:
        data = get_data_by_title(title)
        return data['plot']
    except:
        return f"Failed to retrieve plot for {title}. Title might be incorrect"

def get_rating(title):
    try:
        data = get_data_by_title(title)
        return data['rating']
    except:
        return f"Failed to retrieve rating for {title}. Title might be incorrect"

def get_cast(title):
    try:
        data = get_data_by_title(title)
        return f"{', '.join(data['cast'])}"
    except:
        return f"Failed to retrieve cast for {title}. Title might be incorrect"

def get_characters(title):
    try:
        data = get_data_by_title(title)
        return f"{', '.join(data['characters'])}"
    except:
        return f"Failed to retrieve characters for {title}. Title might be incorrect"
