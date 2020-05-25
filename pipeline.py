#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 17:03:23 2020

@author: josh

This pipeline takes an a topic or topics (any number equal or greater than 1) and returns the new comments for each subbredit where the topic was found

"""

import reddata as rd
import praw

config = rd.load_config()

topics_list = config["topics"]
number_comments = config["comments"]

reddit = praw.Reddit("reddit")

subs_array = rd.get_subreddit_names(reddit, topics_list)

database = rd.get_subreddit_data(reddit, subs_array, number_comments)
