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
    subreddit_data["auth"] = subreddit_data.author.apply(lambda x: x.name)

    final_data = pd.merge(left=database, right=users,on="Index", how="inner")
    
    return final_data
    

combine_subredit_data(database, users)

h =  pd.concat([database, users], axis=1, join="outer")


users = get_redditor_data(database.author)

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
        try:
            print(red)
            topics_dict["name"].append(red.name)
            topics_dict["created_utc"].append(red.created_utc)
            topics_dict["has_subscribed"].append(red.has_subscribed)
            topics_dict["link_karma"].append(red.link_karma)
        except NameError:
            topics_dict["name"].append(None)
            topics_dict["created_utc"].append(None)
            topics_dict["has_subscribed"].append(None)
            topics_dict["link_karma"].append(None)
            

    topics_data = pd.DataFrame(topics_dict)
    return topics_data
