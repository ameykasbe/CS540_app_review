import uuid
import numpy as np
import pandas as pd
from app_store_scraper import AppStore
from google_play_scraper import Sort, reviews
import os
import time

def fetch_reviews_to_csv_play_store(app_name, play_store_app_id, number_of_reviews, export_file_name):
    g_reviews, _ = reviews(
        play_store_app_id,
        lang='en',  # defaults to 'en'
        country='us',  # defaults to 'us'
        sort=Sort.NEWEST,  # defaults to Sort.MOST_RELEVANT
        count = number_of_reviews
    )

    g_df = pd.DataFrame(np.array(g_reviews), columns=['review'])
    g_df2 = g_df.join(pd.DataFrame(g_df.pop('review').tolist()))

    # g_df2.drop(columns=['userImage', 'reviewCreatedVersion'], axis=1, inplace=True)
    g_df2.rename(columns={'score': 'rating', 'userName': 'user_name', 'reviewId': 'review_id', 'content': 'review_description',
                          'at': 'review_date', 'replyContent': 'developer_response', 'repliedAt': 'developer_response_date',
                          'thumbsUpCount': 'thumbs_up'}, inplace=True)
    g_df2.insert(loc=0, column='source', value='Google Play')
    g_df2.insert(loc=0, column='appName', value=app_name)
    # g_df2.insert(loc=3, column='review_title', value=None)
    g_df2['language_code'] = 'en'
    g_df2['country_code'] = 'us'

    export_file_name_play_store = export_file_name + "_play_store.csv"
    g_df2.to_csv(export_file_name_play_store, mode='a', header=not os.path.exists(export_file_name_play_store))



def fetch_reviews_to_csv_app_store(app_name, app_store_app_id, app_store_name, number_of_reviews, export_file_name):
    a_reviews = AppStore('us', app_store_name, app_store_app_id)
    a_reviews.review(how_many=number_of_reviews)

    a_df = pd.DataFrame(np.array(a_reviews.reviews), columns=['review'])
    a_df2 = a_df.join(pd.DataFrame(a_df.pop('review').tolist()))

    # a_df2.drop(columns={'isEdited'}, inplace=True)
    a_df2.insert(loc=0, column='source', value='App Store')
    a_df2.insert(loc=0, column='appName', value=app_name)
    a_df2['developer_response_date'] = None
    a_df2['thumbs_up'] = None
    a_df2['laguage_code'] = 'en'
    a_df2['country_code'] = 'us'
    a_df2.insert(loc=1, column='review_id', value=[
        uuid.uuid4() for _ in range(len(a_df2.index))])
    a_df2.rename(columns={'review': 'review_description', 'userName': 'user_name', 'date': 'review_date',
                          'title': 'review_title', 'developerResponse': 'developer_response'}, inplace=True)
    a_df2 = a_df2.where(pd.notnull(a_df2), None)

    # result = pd.concat([g_df2, a_df2])
    export_file_name_app_store = export_file_name + "_app_store.csv"
    a_df2.to_csv(export_file_name_app_store, mode='a', header=not os.path.exists(export_file_name_app_store))



def fetch_reviews_to_csv(app_name, play_store_app_id, app_store_app_id, app_store_name, number_of_reviews, export_file_name):
    fetch_reviews_to_csv_play_store(app_name, play_store_app_id, number_of_reviews, export_file_name)
    # fetch_reviews_to_csv_app_store(app_name, app_store_app_id, app_store_name, number_of_reviews, export_file_name)

    
    