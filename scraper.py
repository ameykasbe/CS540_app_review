import csv
from util import *
import pathlib
import os

path = pathlib.Path(__file__).parent / 'csv'
children = path.glob('**/*')
file_paths = [file for file in children if file.is_file() and ".csv" in file.name]

check_set = set()

for file in file_paths:
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            app_name = row[0]
            play_store_app_id = row[1]
            app_store_app_id = row[2]
            app_store_name = row[3]
            
            check_set.add(row[0])
            # print(row[0], row[1], row[2], row[3])
print(len(check_set))
            # play_store_app_id = "com.instagram.android"
            # app_store_app_id = "389801252"
            # app_store_name = "com.burbn.instagram"
            # number_of_reviews = 2000 # MUST BE Multiple of 20
            # export_file_name = "entertainment"
            # fetch_reviews_to_csv(play_store_app_id = play_store_app_id, 
            #                         app_store_app_id = app_store_app_id,
            #                         app_store_name = app_store_name,
            #                         number_of_reviews = number_of_reviews,
            #                         export_file_name = export_file_name)