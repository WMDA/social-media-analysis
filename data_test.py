
import praw
import pandas as pd
import reddata as rd
reddit = praw.Reddit("reddit")

reddit_data = rd.get_reddit(["cats"], 5)

comment = rd.get_comments( reddit_object = reddit , ids= reddit_data.id)
