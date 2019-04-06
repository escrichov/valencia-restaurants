import gspread
import json
import os
from jinja2 import Environment, FileSystemLoader
from oauth2client.service_account import ServiceAccountCredentials

# https://developers.google.com/apis-explorer/?hl=es#p/drive/v3/
# https://developers.google.com/identity/protocols/OAuth2ServiceAccount#delegatingauthority
# Share document to the email of service account
# Admin permissions: https://console.cloud.google.com/iam-admin/serviceaccounts?project=food-restaurants-236518
# gspread https://github.com/burnash/gspread
# Example template: https://table2site.com/site/valenciafood

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID')

# Authorization
import time
start = time.time()
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials_service.json', scope)
gc = gspread.authorize(credentials)

# Open a worksheet from spreadsheet with one shot
sh = gc.open_by_key(SPREADSHEET_ID)
wks = sh.worksheet("DB")
end = time.time()

class Restaurant():
    title = None
    image = None
    imageplace = None
    description = None
    zone = None
    price = None
    menu = None
    tags = []
    zones = []
    booking = None
    web = None
    tripadvisor = None
    instagram = None
    googlemaps = None

    def __init__(self, titles, row):
        for title, column in zip(titles, row):
            if title.endswith('-list'):
                item_list = [item.strip() for item in column.split(',') if item != '']
                item_list.sort()
                name = title.replace('-list', '').strip()
                value = item_list
            else:
                name = title.strip()
                value = column.strip()
            setattr(self, name, value)
        self.filters_json = json.dumps(self.tags + self.zones)
        self.images = []
        if self.image:
            self.images.append(self.image)
        if self.imageplace:
            self.images.append(self.imageplace)
        self.images_json = json.dumps(self.images)


def get_all_tags(restaurants, tag_column=5):
    tags = set()
    for restaurant in restaurants:
        tags.update(restaurant.tags)

    return list(tags)

def get_all_zones(restaurants, zone_column=3):
    zones = set()
    for restaurant in restaurants:
        zones.update(restaurant.zones)

    return list(zones)

# Get all restaurants
cell_list = wks.get_all_values()
titles = cell_list[0]
restaurants = [Restaurant(titles, row) for row in cell_list[1:]]
tags = get_all_tags(restaurants)
tags.sort()
zones = get_all_zones(restaurants)
zones.sort()

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('main.html')
output_from_parsed_template = template.render({'restaurants': restaurants, 'tags': tags, 'zones': zones})

with open("index.html", "w") as fh:
    fh.write(output_from_parsed_template)
