from util import *
import pathlib
from serpapi import GoogleSearch

apps_not_present = ["Flashlight & LED Torch"]

strs = "Resilio Sync,com.cleanmaster.security,917410266,sync-secure-cloud-storage"

row = strs.split(",")

app_name = row[0]
play_store_app_id = row[1]
app_store_app_id = row[2]
app_store_name = row[3]
number_of_reviews = 200 # MUST BE Multiple of 20

file = pathlib.Path(__file__).parent / 'csv' / 'tools.csv'

fetch_reviews_to_csv(app_name = app_name,
                    play_store_app_id = play_store_app_id, 
                    app_store_app_id = app_store_app_id,
                    app_store_name = app_store_name,
                    number_of_reviews = number_of_reviews,
                    export_file_name = file.name[:-4])