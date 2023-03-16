import uuid

import numpy as np
import pandas as pd
from app_store_scraper import AppStore
from google_play_scraper import Sort, reviews

NUMBER_OF_REVIEWS = 100 # MUST BE Multiple of 20

if __name__ == "__main__":
    g_reviews, _ = reviews(
        "com.instagram.android",
        lang='en',  # defaults to 'en'
        country='us',  # defaults to 'us'
        sort=Sort.NEWEST,  # defaults to Sort.MOST_RELEVANT
        count = NUMBER_OF_REVIEWS
    )

    a_reviews = AppStore('us', 'instagram', '389801252')
    a_reviews.review(how_many=NUMBER_OF_REVIEWS)


    g_df = pd.DataFrame(np.array(g_reviews), columns=['review'])
    g_df2 = g_df.join(pd.DataFrame(g_df.pop('review').tolist()))

    g_df2.drop(columns={'userImage', 'reviewCreatedVersion'}, inplace=True)
    g_df2.rename(columns={'score': 'rating', 'userName': 'user_name', 'reviewId': 'review_id', 'content': 'review_description',
                          'at': 'review_date', 'replyContent': 'developer_response', 'repliedAt': 'developer_response_date',
                          'thumbsUpCount': 'thumbs_up'}, inplace=True)
    g_df2.insert(loc=0, column='source', value='Google Play')
    g_df2.insert(loc=3, column='review_title', value=None)
    g_df2['language_code'] = 'en'
    g_df2['country_code'] = 'us'

    a_df = pd.DataFrame(np.array(a_reviews.reviews), columns=['review'])
    a_df2 = a_df.join(pd.DataFrame(a_df.pop('review').tolist()))

    a_df2.drop(columns={'isEdited'}, inplace=True)
    a_df2.insert(loc=0, column='source', value='App Store')
    a_df2['developer_response_date'] = None
    a_df2['thumbs_up'] = None
    a_df2['laguage_code'] = 'en'
    a_df2['country_code'] = 'us'
    a_df2.insert(loc=1, column='review_id', value=[
        uuid.uuid4() for _ in range(len(a_df2.index))])
    a_df2.rename(columns={'review': 'review_description', 'userName': 'user_name', 'date': 'review_date',
                          'title': 'review_title', 'developerResponse': 'developer_response'}, inplace=True)
    a_df2 = a_df2.where(pd.notnull(a_df2), None)

    result = pd.concat([g_df2, a_df2])
    result.to_csv("instagram_100.csv")

