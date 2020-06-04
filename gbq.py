import base64
import datetime
import pandas as pd
import pandas_gbq
import praw

def cache_reddit_data(event, context):
    """
    Stores reddit data
    """

    current_data = collect_reddit_data()

    current_data["backup_date"] = datetime.date.today()

    current_data["backup_time"] = datetime.datetime.today().time()

    pandas_gbq.to_gbq(current_data, "reddit-276014.reddit_test", project_id="reddit-276014", if_exists="append")

    return None

def collect_reddit_data():

    """
    collect reddit data and outputs a pandas dataframe
    """

    comments_number = 5
    topics_list = ["cats"]

    reddit = praw.Reddit(client_id='RNGhJE66F0dfcg',
                     client_secret='reMSAKkNv5daoHSRG3Cy15BhVw8',
                     user_agent='cdc')

    subs_array = rd.get_subreddit_names(reddit, topics_list)

    database = rd.get_subreddit_data(reddit, subs_array, comments= comments_number, sort="new"  )

    return(database)
