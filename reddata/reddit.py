#!/usr/bin/env python3
import pandas as pd
import praw
import reddata as rd

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


def add_reddit_data(df):
    """
    Adds the latest reddit to the existing data and drops any non-unique values

    Parameters
    ----------
    df : dataframes list
        2 or more dataframes given as an array

    Returns
    -------
    Pandas dataframe with only unique values

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
                        "id":[], \
                         "url":[], \
                        "comms_num": [], \
                        "created": [], \
                        "body":[], \
                        "subreddit": [],
                        "author": [],
                        "comments": []
                  }

    sub_list = subs


    for sub in sub_list:

        print('\nWorking on this sub right now: \n', sub)

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


def get_reddit(topics_list, comments_number, reddit_inst= "env"):
    """
    A wrapper for other disinfo functions to collect reddit data

    Parameters
    ----------
    reddit_inst : TYPE
        DESCRIPTION.
    topics_list : TYPE
        DESCRIPTION.
    comments_number : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """

    if reddit_inst == "env":
        reddit = praw.Reddit("reddit")
    else:
        reddit = reddit_inst

    subs_array = rd.get_subreddit_names(reddit, topics_list)

    database = rd.get_subreddit_data(reddit, subs_array, comments= comments_number, sort="new"  )

    users = rd.get_redditor_data(database.author)

    final_data = pd.concat([database, users], axis=1, join="outer")

    return final_data
