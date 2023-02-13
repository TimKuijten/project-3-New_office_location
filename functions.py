from pymongo import MongoClient
import pandas as pd
import folium
from folium import Choropleth, Circle, Marker, Icon, Map, TileLayer
from folium.plugins import HeatMap, MarkerCluster
import random
import requests
import json
import geopandas as gpd

#Set connection to mongoDB
def mongo_connection(database,collection):
    client = MongoClient("localhost:27017")
    db = client[f"{database}"]
    client.list_database_names()
    global c 
    c = db.get_collection(f"{collection}")

# This function gets data from foursquare and returns it in a DF 
def get_foursquare_data():
    base_url = "https://api.foursquare.com/v3/places/search"
    locations = (list_dict_locations)
    headers = {
        "accept": "application/json",
        "Authorization": token
    }
    data_frames = []
    for location in locations:
        links = [
            f"query=school&ll={location['lat']}%2C{location['long']}&radius=1000",
            f"ll={location['lat']}%2C{location['long']}&radius=500&chains=ab4c54c0-d68a-012e-5619-003048cad9da",
            f"ll={location['lat']}%2C{location['long']}&radius=1000&categories=10032",
            f"ll={location['lat']}%2C{location['long']}&radius=500&categories=13377",
            f"ll={location['lat']}%2C{location['long']}&radius=10000&categories=18008",
            f"ll={location['lat']}%2C{location['long']}&radius=1000&categories=11134"
        ]
        counts = []
        for link in links:
            url = f"{base_url}?{link}"
            response = requests.get(url, headers=headers)
            count = len(response.json().get("results", []))
            counts.append(count)
        df = pd.DataFrame({"Category": ["Schools 1km", "Starbucks 500m", "Night Clubs 1km", "Vegan Restaurants 500m", "Basketball Courts 10km", "Pet Grooming Services 1km"], "Count": counts})
        df["Location"] = location["name"]
        data_frames.append(df)
    return pd.concat(data_frames).pivot(index="Location", columns="Category", values="Count")



# # # # # # # # # # # # # # # # ADD MARKERS TO MAPS

# This function returns a dict 
def name_coordinates (dict_):
    
    processed_dict = {"name": dict_["name"],
                     "lat": dict_["geocodes"]["main"]["latitude"],
                     "lon": dict_["geocodes"]["main"]["longitude"]}
    
    return processed_dict


# This function uses the foursquare api to look for train/metro/airport within a 25km radius and adds them to a map
def map_public_transport(city):

        # Train station
        url = "https://api.foursquare.com/v3/places/search?ll=1.244463%2C103.834701&radius=25000&categories=19047"

        headers = {
            "accept": "application/json",
            "Authorization": "fsq3wrzINxzk4PynA7gLZ5EdvOrLwygPimqKwxWyEORriC4="
        }

        response = requests.get(url, headers=headers)
        train_list = []
        for i in response.json()["results"]:
            train_list.append(name_coordinates(i))
        
        df_train = pd.DataFrame(train_list)

        for index, row in df_train.iterrows():
            icon = Icon(
            color = "gray",
            fill_opacity = 0.5,
            prefix = "fa",
            icon = 'train',
            icon_color = "white"
        )
            folium.Marker([row['lat'], row['lon']], popup=row['name'], icon=icon).add_to(singapore_map)

        # Airport
        url = "https://api.foursquare.com/v3/places/search?query=Airport&near=Singapore&limit=1"


        headers = {
            "accept": "application/json",
            "Authorization": "fsq3wrzINxzk4PynA7gLZ5EdvOrLwygPimqKwxWyEORriC4="
        }

        response = requests.get(url, headers=headers)
        airport_list = []
        for i in response.json()["results"]:
            airport_list.append(name_coordinates(i))
        
        df_airport = pd.DataFrame(airport_list)

        for index, row in df_airport.iterrows():
            icon = Icon(
            color = "gray",
            fill_opacity = 0.5,
            prefix = "fa",
            icon = 'plane',
            icon_color = "white"
        )
            folium.Marker([row['lat'], row['lon']], popup=row['name'], icon=icon).add_to(singapore_map)
        # Metro
        url = "https://api.foursquare.com/v3/places/search?ll=1.244463%2C103.834701&radius=25000&categories=19046"

        headers = {
            "accept": "application/json",
            "Authorization": "fsq3wrzINxzk4PynA7gLZ5EdvOrLwygPimqKwxWyEORriC4="
        }

        response = requests.get(url, headers=headers)
        metro_list = []
        for i in response.json()["results"]:
            metro_list.append(name_coordinates(i))
        
        df_metro = pd.DataFrame(metro_list)

        for index, row in df_metro.iterrows():
            icon = Icon(
            color = "gray",
            fill_opacity = 0.5,
            prefix = "fa",
            icon = 'subway',
            icon_color = "white"
        )
            folium.Marker([row['lat'], row['lon']], popup=row['name'], icon=icon).add_to(singapore_map)

            # Metro
        url = "https://api.foursquare.com/v3/places/search?query=Train%20station&ll=1.244463%2C103.834701&radius=25000"

        headers = {
            "accept": "application/json",
            "Authorization": "fsq3wrzINxzk4PynA7gLZ5EdvOrLwygPimqKwxWyEORriC4="
        }

        response = requests.get(url, headers=headers)
        tram2_list = []
        for i in response.json()["results"]:
            tram2_list.append(name_coordinates(i))
        
        df_tram2 = pd.DataFrame(tram2_list)

        for index, row in df_tram2.iterrows():
            icon = Icon(
            color = "gray",
            fill_opacity = 0.5,
            prefix = "fa",
            icon = 'train',
            icon_color = "white"
        )
            folium.Marker([row['lat'], row['lon']], popup=row['name'], icon=icon).add_to(singapore_map)

# This function looks for schools, starbucks, nightclubs, vegan restaurants, basketball courts and and groomers within
# a certan area
def add_places_to_map(locationslist):
    locations = locationslist
    headers = {
        "accept": "application/json",
        "Authorization": token
    }
    for location in locations:
        lat = location["lat"]
        lon = location["long"]

        # Schools 1000m
        url = f"https://api.foursquare.com/v3/places/search?query=school&ll={lat}%2C{lon}&radius=1000"

        headers = {
            "accept": "application/json",
            "Authorization": token 
        }

        response = requests.get(url, headers=headers)

        school_list = []
        for i in response.json()["results"]:
            school_list.append(name_coordinates(i))
        
        df_school = pd.DataFrame(school_list)

        for index, row in df_school.iterrows():
            icon = Icon(
            color = "red",
            prefix = "fa",
            icon = 'book',
            icon_color = "white"
        )
            folium.Marker([row['lat'], row['lon']], popup=row['name'], icon=icon).add_to(singapore_map)
# Starbucks 500m
        url = f"https://api.foursquare.com/v3/places/search?ll={lat}%2C{lon}&radius=500&chains=ab4c54c0-d68a-012e-5619-003048cad9da"

        headers = {
            "accept": "application/json",
            "Authorization": token
        }

        response = requests.get(url, headers=headers)

        starbucks_list = []
        for i in response.json()["results"]:
            starbucks_list.append(name_coordinates(i))
        
        df_starbucks = pd.DataFrame(starbucks_list)

        for index, row in df_starbucks.iterrows():
            icon = Icon(
            color = "beige",
            prefix = "fa",
            icon = 'coffee',
            icon_color = "white"
        )
            folium.Marker([row['lat'], row['lon']], popup=row['name'], icon=icon).add_to(singapore_map)
# Nightclub 1km
        url = f"https://api.foursquare.com/v3/places/search?ll={lat}%2C{lon}&radius=1000&categories=10032"

        headers = {
            "accept": "application/json",
            "Authorization": token
        }

        response = requests.get(url, headers=headers)

        nightclub_list = []
        for i in response.json()["results"]:
            nightclub_list.append(name_coordinates(i))
        
        df_nightclub = pd.DataFrame(nightclub_list)

        for index, row in df_nightclub.iterrows():
            icon = Icon(
            color = "purple",
            prefix = "fa",
            icon = 'music',
            icon_color = "white"
        )
            folium.Marker([row['lat'], row['lon']], popup=row['name'], icon=icon).add_to(singapore_map)

        #Vegan restaurant 500m
        url = f"https://api.foursquare.com/v3/places/search?ll={lat}%2C{lon}&radius=500&categories=13377"

        headers = {
        "accept": "application/json",
        "Authorization": token
        }

        response = requests.get(url, headers=headers)

        vegan_rest_list = []
        for i in response.json()["results"]:
            vegan_rest_list.append(name_coordinates(i))

        vegan_rest_list = []
        for i in response.json()["results"]:
            vegan_rest_list.append(name_coordinates(i))
            
        df_vegan_rest = pd.DataFrame(vegan_rest_list)

        for index, row in df_vegan_rest.iterrows():
            icon = Icon(
            color = "black",
            #opacity = 0.1,
            prefix = "fa", #font-awesome
            icon = 'cutlery',
            icon_color = "white"
        )
            folium.Marker([row['lat'], row['lon']], popup=row['name'], icon=icon).add_to(singapore_map)

        #Basketball 10km
        url = f"https://api.foursquare.com/v3/places/search?ll={lat}%2C{lon}&radius=10000&categories=18008"

        headers = {
        "accept": "application/json",
        "Authorization": token
        }

        response = requests.get(url, headers=headers)

        basketball_list = []
        for i in response.json()["results"]:
            basketball_list.append(name_coordinates(i))
            
        df_basketball = pd.DataFrame(basketball_list)

        for index, row in df_basketball.iterrows():
            icon = Icon(
            color = "orange",
            #opacity = 0.1,
            prefix = "fa", #font-awesome
            icon = 'futbol',
            icon_color = "white"
        )
            folium.Marker([row['lat'], row['lon']], popup=row['name'], icon=icon).add_to(singapore_map)

        #Groomer 1km
        url = f"https://api.foursquare.com/v3/places/search?ll={lat}%2C{lon}&radius=1000&categories=11134"

        headers = {
        "accept": "application/json",
        "Authorization": token
        }

        response = requests.get(url, headers=headers)

        groomer_list = []
        for i in response.json()["results"]:
            groomer_list.append(name_coordinates(i))
            
        df_groomer = pd.DataFrame(groomer_list)

        for index, row in df_groomer.iterrows():
            icon = Icon(
            color = "green",
            #opacity = 0.1,
            prefix = "fa", #font-awesome
            icon = 'paw',
            icon_color = "white"
        )
            folium.Marker([row['lat'], row['lon']], popup=row['name'], icon=icon).add_to(singapore_map)
        return singapore_map



# # # # # # # # # # # # # # # # WEB SCRAPING


# This function is webscraping to rent offices in Signapore (www.99.co)
def get_sgp_office_data(start, end):
    sgp_office_data = []
    for offset in range(start, end):
        url = f'https://www.99.co/singapore/commercial/rent/offices?listing_type=rent&main_category=office&map_bounds=1.5827095153768858%2C103.49449749970108%2C1.1090706240313446%2C104.12483807587296&page_num={offset}&page_size=35&path=%2Fsingapore%2Fcommercial%2Frent%2Foffices&property_segments=commercial&query_coords=1.3039947%2C103.8298507&query_limit=radius&query_type=city&radius_max=1000&rental_type=unit&show_cluster_preview=true&show_description=true&show_internal_linking=true&show_meta_description=true&show_nearby=true&zoom=15'
        html = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
        soup = BeautifulSoup(html.content, "html.parser")
        
        tags_name = soup.find_all("a", class_="_3Ajbv _30I97 _1vzK2", href=True)
        tags_district = soup.find_all("li", class_="_3WG9R", href=False, attrs={"itemprop": "addressRegion"})
        tags_address = soup.find_all("li", class_="_3WG9R _3L5OV", attrs={"itemprop": "streetAddress"})
        tags_price = soup.find_all("li", class_="JlU_W")
        tags_size = soup.find_all("li", class_="_1x-U1")
        tags_link = soup.find_all("a", href=True)

        # Extract the text values from the tags
        names = [i.text.replace("Office in ", "").strip() for i in tags_name]
        districts = [i.text.strip() for i in tags_district]
        addresses = [i.text.strip() for i in tags_address]
        prices = [i.text.strip().replace(",", "").replace("[", "").replace("]", "").replace("$", "").split("/")[0] for i in tags_price]
        sizes = [i.text.strip().replace(",", "").replace("[", "").replace("]", "").split("/")[0].split(" ")[0] for i in tags_size]
        links = [i['href'] for i in tags_link if 'enquiry_source' in i['href']]
        # Zip the values together
        rows = list(zip(names, districts, addresses, prices, sizes, links))
        sgp_office_data.extend(rows)
        
    df_sgp_office = pd.DataFrame(sgp_office_data, columns=['Name', 'District', 'Address', 'Price ($) p/m', 'Size (m2)', 'Link'])
    df_sgp_office['Price per m2'] =  (df_sgp_office['Price ($) p/m'].astype(float) / df_sgp_office['Size (m2)'].astype(float)).round(2)
    df_sgp_office['Link'] = df_sgp_office['Link'].apply(lambda x: 'https://www.99.co' + x)
    df_sgp_office = df_sgp_office.reindex(columns=[i for i in df_sgp_office.columns if i != 'Link'] + ['Link'])

    return df_sgp_office

#This function uses Geocode to add coordinates to DF of locations without coordinates
def add_coordinates_to_dataframe(df):
    for index, row in df.iterrows():
        address = row['Address']
        name = row['Name']
        url = f'https://geocode.xyz/{address} {name} Singapore?json=1'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            try:
                latitude = float(data['latt'])
                longitude = float(data['longt'])
                df.loc[index, 'Latitude'] = latitude
                df.loc[index, 'Longitude'] = longitude
            except KeyError:
                print(f"No match for {address}")
        else:
            print(f"Error getting coordinates for {address}")



