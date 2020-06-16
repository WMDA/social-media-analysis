#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 11:06:50 2020

@author: josh
"""


def combine_subredit_data(subreddit_data, subreddit_author):
    """
    

    Parameters
    ----------
    dataset1 : TYPE
        DESCRIPTION.
    dataset2 : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    if (subreddit_data.index[-1] -1 == len(subreddit_data)) == False:
        subreddit_data = subreddit_data.reset_index()
        print("Resetting index")
    
    auth = np.array(subreddit_data.author)
 
    names = np.array(subreddit_author.name)
    
    dict = {'auth': []}
    
    for i in auth:
        dict["auth"].append(i.name)
    
    
    column_names = ['author', 'created_utc', 'has_subscribed', 'link_karma']
    
    
    final_data = pd.concat([subreddit_data, subreddit_author], axis=1, join="outer")
    
    
    pd.concat([dataframe1, dataframe4], axis=1 )