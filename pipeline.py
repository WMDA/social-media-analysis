#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 17:03:23 2020

@author: josh

This pipeline takes an a topic or topics (any number equal or greater than 1) and returns the new comments for each subbredit where the topic was found

"""

import reddata as rd
import praw
import pandas as pd

options= rd.get_arguments()
topics_list = options.topics
number_comments = int(options.comments)

rd.print_output(topics_list,number_comments)

reddit = praw.Reddit("reddit")

subs_array = rd.get_subreddit_names(reddit, topics_list)

database = rd.get_subreddit_data(reddit, subs_array, number_comments)

if options.csv and not options.name:
    database.to_csv("%s/reddit_database.csv" % options.csv, encoding='utf-8', index=False)
elif options.csv and options.name:
    database.to_csv("%s/%s.csv" % (options.csv,options.name), encoding='utf-8', index=False)
elif options.name and not options.csv:
    print("WARNING: File name given but directory was not given. Results were not saved to file format.",'\n',"Use -h or --help for support")
elif not options.csv and not options.name:
    print("WARNING: No flag to save results to a file was given." '\n',"Use -h or --help for support or go to https://github.com/WMDA/social-media-analysis")
