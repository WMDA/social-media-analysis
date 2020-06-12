#!/usr/bin/env python3
import pandas as pd

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



def get_subreddit_data(reddit_object, subs, comments, sort='new'):
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
                        "subreddit": [] ,\
                        "author":[],\
                        "permalink":[]
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
            topics_dict["permalink"].append(submission.permalink)

        topics_comment={"comment_author":[], \
                        "id_from_thread":[], \
                        "comment_body":[], \
                     "comment_permalink":[],\
                     "comment_score":[]}
        
        for url_id in topics_dict['id']:
            try:
                submission= reddit.submission(id=url_id)
                submission.comments.replace_more(limit=None)
                for comment in submission.comments.list():
                        topics_comment['comment_body'].append(comment.body)
                        topics_comment['id_from_thread'].append(url_id)
                        topics_comment['comment_author'].append(comment.author)
                        topics_comment['comment_permalink'].append(comment.permalink)
                        topics_comment['comment_score'].append(comment.score)
            except HTTPException:
                    print('Error unable to collect comments due to HTTPException')
                    continue

    topics_data = pd.DataFrame(topics_dict)
    comments_data= pd.DataFrame(topics_comment)
    return topics_data, comments_data
