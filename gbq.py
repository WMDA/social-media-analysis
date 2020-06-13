import base64
import pandas as pd
import pandas_gbq
import praw
import datetime

# Cloud function config
project_id = ""
table_sub = ""
table_com =
reddit = praw.Reddit(client_id='RNGhJE66F0dfcg',
                     client_secret='reMSAKkNv5daoHSRG3Cy15BhVw8',
                     user_agent='cdc')
comments_number = 1000
topics_list = [""]


def cache_reddit_data(event, context):
    """
    Stores reddit data
    """

    pubsub_message = base64.b64decode(event['data']).decode('utf-8')

    # get the data to store

    current_data = get_reddit(topics_list, comments_number)
    current_data["created"] = current_data["created"].apply(convert_date)
    current_data["backup_date"] = datetime.date.today()
    current_data["backup_time"] = datetime.datetime.today().time()

    # find the earliest and latest date, used in the SQL query to check for duplicates

    earliest_date = min(current_data["created"].apply(convert_date))
    earliest_date_string =  earliest_date.strftime("%Y-%m-%d")

    latest_date = max(current_data["created"].apply(convert_date))
    latest_date_string =  latest_date.strftime("%Y-%m-%d")

    sql = "SELECT * FROM {0} WHERE backup_date > {1} AND backup_date < {2}"
    SQL = sql.format(table, earliest_date_string, latest_date_string)

    # obtain data from the same period to check for duplciates
    df = pandas_gbq.read_gbq(query=SQL, project_id=project_id)

    # Remove duplcates
    unique_data = merge_data_unique(df, current_data)

    # Add data to bigquery
    pandas_gbq.to_gbq(unique_data, table_sub, project_id=project_id, if_exists="append")

    # Get the comments data
    comment_data = get_comments(reddit, unique_data.id)

    # add the comment data to a seperate gbq table
    pandas_gbq.to_gbq(comment_data, table_com, project_id=project_id, if_exists="append")

    return None

# function to get data, adapted from package function
def get_reddit(topics_list, comments_number):

    reddit = reddit

    subs_array = get_subreddit_names(reddit, topics_list)

    database = get_subreddit_data(reddit, subs_array, comments= comments_number, sort="new"  )

    users = get_redditor_data(database.author)

    final_data = pd.concat([database, users], axis=1, join="outer")

    return final_data


### ============================================================ ###
#  All functions below are taken directly from the package reddata #
### ============================================================ ###

def get_subreddit_names(reddit_object, search_terms):

    reddit = reddit_object

    topics_dict = {
                        "subreddit": []
                  }

    topic_list = search_terms

    for topic in topic_list:

        cont_subreddit = reddit.subreddit("all").search(topic)

        for submission in cont_subreddit:
                topics_dict["subreddit"].append(submission.subreddit)

    data = pd.DataFrame(topics_dict)

    data = data["subreddit"].apply(str).unique()

    return data


def get_subreddit_data(reddit_object, subs, comments= 10, sort='new'):
    """
        Get Subreddit data
        Parameters
        ----------
        reddit_object : stuffs
        Returns
        -------
        Pandas Dataframe
    """

    reddit = reddit_object

    topics_dict = {     "title":[], \
                        "score":[], \
                        "id":[], "url":[], \
                        "comms_num": [], \
                        "created": [], \
                        "body":[], \
                        "subreddit": [],
                        "author": [],
                        "comments": []
                  }

    sub_list = subs

    for sub in sub_list:

        print('Working on this sub right now: \n', sub)

        subreddit = reddit.subreddit(sub)

        submission_dict ={'new':subreddit.new, \
                          'controversial':subreddit.controversial,\
                          'gilded':subreddit.gilded,\
                          'hot':subreddit.hot,\
                          'rising':subreddit.rising,\
                          'top':subreddit.top }


        cont_subreddit = submission_dict[sort](limit=comments)

        for submission in cont_subreddit:
            topics_dict["title"].append(submission.title)
            topics_dict["score"].append(submission.score)
            topics_dict["id"].append(submission.id)
            topics_dict["url"].append(submission.url)
            topics_dict["comms_num"].append(submission.num_comments)
            topics_dict["created"].append(submission.created)
            topics_dict["body"].append(submission.selftext)
            topics_dict["subreddit"].append(submission.subreddit)
            topics_dict["author"].append(submission.author)
            topics_dict["comments"].append(submission.comments)

    topics_data = pd.DataFrame(topics_dict)
    return topics_data

def get_redditor_data(redditors):
    """
    Given a array of redditors will return attrbutes of each redditor

    Parameters
    ----------
    def get_redditor_data : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """


    topics_dict = { "name": [],
                    "created_utc": [],
                    "has_subscribed": [],
                    "link_karma": []
                    }

    for red in redditors:
        topics_dict["name"].append(red.name)
        topics_dict["created_utc"].append(red.created_utc)
        topics_dict["has_subscribed"].append(red.has_subscribed)
        topics_dict["link_karma"].append(red.link_karma)

    topics_data = pd.DataFrame(topics_dict)
    return topics_data



def get_comments(reddit_object, ids):
    """
    Given an array of ids for submissions collect comments from each submission

    Returns
    -------
    None.

    """
    reddit = reddit_object

    topics_dict ={"comment_author":[], \
                  "id_from_thread":[], \
                  "comment_body":[], \
                  "comment_permalink":[],\
                  "comment_score":[]}


    for i in ids:

        submission = reddit.submission(id=i)
        submission.comments.replace_more(limit=None)

        for comment in submission.comments.list():
            topics_dict['comment_body'].append(comment.body)
            topics_dict['id_from_thread'].append(i)
            topics_dict['comment_author'].append(comment.author)
            topics_dict['comment_permalink'].append(comment.permalink)
            topics_dict['comment_score'].append(comment.score)

    topics_data = pd.DataFrame(topics_dict)
    return topics_data

def convert_date(x):
    '''
    Converts the date column from the reddit api into standard format
    '''
    return dt.datetime.fromtimestamp(x)


def merge_data_unique(dataset1, dataset2):
    """
    Merged two datasets returning only unique values

    Returns
    -------
    None.

    """

    merged = pd.merge(left=dataset1, right=dataset2, how="inner")

    return merged
