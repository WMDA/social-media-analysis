import praw
import pandas as pd
import datetime as dt
import pprint

def get_date(created):
    return dt.datetime.fromtimestamp(created)

reddit = praw.Reddit(client_id='s_HcoGxQGc7a8A', \
                     client_secret='dOnPnAYpEhopn3Fgxgh5JPKZH4o', \
                     user_agent='Rudacus' )

subreddit=reddit.subreddit('VERYBADWIZARDS')
#print(subreddit.description)


topics_dict = {"title":[], \
                "score":[], \
                "id":[], "url":[], \
                "comms_num": [], \
                "created": [], \
                "body":[]}

for submission in subreddit.(limit=None):
    topics_dict["title"].append(submission.title)
    topics_dict["score"].append(submission.score)
    topics_dict["id"].append(submission.id)
    topics_dict["url"].append(submission.url)
    topics_dict["comms_num"].append(submission.num_comments)
    topics_dict["created"].append(submission.created)
    topics_dict["body"].append(submission.selftext)


df = pd.DataFrame(topics_dict)
_timestamp = df["created"].apply(get_date)
df = df.assign(timestamp = _timestamp)

print(df.shape)
'''
top_level_comments = list(submission.comments)
all_comments = submission.comments.list()

print()
print(submission.title) # to make it non-lazy
att = (vars(submission))
pprint.pprint(att.keys())
'''
