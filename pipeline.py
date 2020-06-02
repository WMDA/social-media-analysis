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

#Takes command line arguments
options= rd.get_arguments()

#Assigns options to variables
topics_list = options.topics
number_comments = int(options.comments)

# Warning messages if file name or no file directory given
if options.name and not options.csv:
    print("WARNING: File name given but directory was not given. Results were not saved to file format.",'\n',"Use -h or --help for support")
elif not options.csv and not options.name:
    print("WARNING: No flag to save results to a file was given." '\n',"Use -h or --help for support or go to https://github.com/WMDA/social-media-analysis")

# Prints ouput of what topics are being searched for
rd.print_output(topics_list,number_comments)

#Calls reddit functions from reddit.py
reddit = praw.Reddit("reddit")
subs_array = rd.get_subreddit_names(reddit, topics_list)
database = rd.get_subreddit_data(reddit, subs_array, number_comments)

# Assigns to results to csv
if options.csv and not options.name:
    database.to_csv("%s/reddit_database.csv" % options.csv, encoding='utf-8', index=False)
elif options.csv and options.name:
    database.to_csv("%s/%s.csv" % (options.csv,options.name), encoding='utf-8', index=False)
