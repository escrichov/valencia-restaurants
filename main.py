import gspread
import json
import os
import sys
from os import listdir
from os.path import isfile, join
from jinja2 import Environment, FileSystemLoader
from oauth2client.service_account import ServiceAccountCredentials
from optimizeimage import optimize_url
import time
import locale


# https://developers.google.com/apis-explorer/?hl=es#p/drive/v3/
# https://developers.google.com/identity/protocols/OAuth2ServiceAccount#delegatingauthority
# Share document to the email of service account
# Admin permissions: https://console.cloud.google.com/iam-admin/serviceaccounts?project=food-restaurants-236518
# gspread https://github.com/burnash/gspread
# Example template: https://table2site.com/site/valenciafood

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID')
TEMPLATES_DIR = 'templates'
OUTPUT_TEMPLATES_DIR = '.'
CACHE_FILE = '.gspread_cache'
locale.setlocale(locale.LC_TIME, "es_ES.utf8")


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
            self.image = optimize_url(self.image, 'images')
            self.images.append(self.image)
        if self.imagefood1:
            self.imagefood1 = optimize_url(self.imagefood1, 'images')
            self.images.append(self.imagefood1)
        if self.imagefood2:
            self.imagefood2 = optimize_url(self.imagefood2, 'images')
            self.images.append(self.imagefood2)
        if self.imagedessert:
            self.imagedessert = optimize_url(self.imagedessert, 'images')
            self.images.append(self.imagedessert)
        if self.imageplace:
            self.imageplace = optimize_url(self.imageplace, 'images')
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

if __name__ == "__main__":
    # Authorization
    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials_service.json', scope)
    gc = gspread.authorize(credentials)

    # Open a worksheet from spreadsheet with one shot
    sh = gc.open_by_key(SPREADSHEET_ID)
    wks = sh.worksheet("DB")

    # Get all cells
    cell_list = wks.get_all_values()
    cell_list_json = json.dumps(cell_list)

    # Decide if cache is changed
    if os.environ.get('ONLY_BUILD_IF_DATA_CHANGES', 'False') == 'True':
        if isfile(CACHE_FILE):
            with open(CACHE_FILE, "r") as fh:
                cell_list_cached = fh.read()
                if cell_list_cached == cell_list_json:
                    print("Build no generated. Data no changed.")
                    sys.exit(1)

    # Cache cells
    with open(CACHE_FILE, "w") as fh:
        fh.write(cell_list_json)

    # Convert cells to Restaurants
    titles = cell_list[0]
    restaurants = [Restaurant(titles, row) for row in cell_list[1:]]
    tags = get_all_tags(restaurants)
    tags.sort()
    zones = get_all_zones(restaurants)
    zones.sort()

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template_files = [f for f in listdir(TEMPLATES_DIR) if isfile(join(TEMPLATES_DIR, f))]
    for f in template_files:
        if f.startswith('template'):
            continue

        template = env.get_template(f)
        context = {
            'restaurants': restaurants,
            'tags': tags,
            'zones': zones,
            'date': time.strftime("%a, %d %b %Y %H:%M:%S"),
        }
        output_from_parsed_template = template.render(context)
        with open(join(OUTPUT_TEMPLATES_DIR, f), "w") as fh:
            fh.write(output_from_parsed_template)
