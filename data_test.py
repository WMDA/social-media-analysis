
import praw
import pandas as pd
import prawcore
reddit = praw.Reddit("reddit")

def get_subreddit_names(reddit_object, search_terms):

    reddit = reddit_object

    topics_dict = {"subreddit": []}
    topic_list = search_terms
    for topic in topic_list:

        cont_subreddit = reddit.subreddit("all").search(topic)

        for submission in cont_subreddit:
                topics_dict["subreddit"].append(submission.subreddit)

    data = pd.DataFrame(topics_dict)
    data = data["subreddit"].apply(str).unique()
    return data


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


    redditors_dict = { "name": [],
                    "created_utc": [],
                    "has_subscribed": [],
                    "link_karma": []
                    }
    for red in redditors:
        try:
            deleted_User_check=str(red)
            print(red)
            if deleted_User_check =='None':
                redditors_dict["name"].append('Deleted_User')
                redditors_dict["created_utc"].append('Deleted_User')
                redditors_dict["has_subscribed"].append('Deleted_User')
                redditors_dict["link_karma"].append('Deleted_User')
            else:
                redditors_dict["name"].append(red.name)
                redditors_dict["created_utc"].append(red.created_utc)
                redditors_dict["has_subscribed"].append(red.has_subscribed)
                redditors_dict["link_karma"].append(red.link_karma)
        except (prawcore.exceptions.NotFound, AttributeError):
            redditors_dict["created_utc"].append('NA')
            redditors_dict["has_subscribed"].append('NA')
            redditors_dict["link_karma"].append('NA')



    redditors_data = pd.DataFrame(redditors_dict)
    return redditors_data

def get_subreddit_data(reddit_object, subs, comments= 10, sort='new'):
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
                          'top':subreddit.top
                           }


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

df=get_subreddit_names(reddit,["anorexia"])
print(len(df))
df1 = get_subreddit_data(reddit,df, comments=1)#, sort='controversial')
df2= get_redditor_data(df1.author)

#print('\rHello:', end='')

#df.to_csv("~/Documents/Codes/social-media/reddit_database.csv", encoding='utf-8', index=False)
#comments.to_csv("~/Documents/Codes/social-media/comments_database.csv", encoding='utf-8', index=False)
#comment = rd.get_comments( reddit_object = reddit , ids= reddit_data.id)
