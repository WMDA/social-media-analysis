
import pytest
import numpy as np
import pandas as pd
import reddata as rd
from pandas._testing import assert_frame_equal
import datetime

dates = np.array(['2005-02-01', '2005-02-02', '2005-02-03', '2005-02-04',
       '2005-02-05', '2005-02-06', '2005-02-07', '2005-02-08',
       '2005-02-09', '2005-02-10', '2005-02-11', '2005-02-12',
       '2005-02-13', '2005-02-14', '2005-02-15', '2005-02-16',
       '2005-02-17', '2005-02-18', '2005-02-19', '2005-02-20',
       '2005-02-21', '2005-02-22', '2005-02-23', '2005-02-24',
       '2005-02-25', '2005-02-26', '2005-02-27', '2005-02-28'],
      dtype='datetime64[D]')


def test_date_range():
    assert rd.date_range(dates)[1] == np.datetime64('2005-02-28')
    assert rd.date_range(dates)[0] == np.datetime64('2005-02-01')


dataframe1 = pd.DataFrame({
      'A': [1,2,3,4,5,6],
      'B': [2,3,4,5,6,7],
      'C': ["hat", "cat", "mat", "sat", "bat", "flat"],
     'ID': ['gxt1bd', 'gxt1f9', 'gxt10i', 'gxt15f', 'gxt0yl', 'gxszzn']
     })



dataframe2 = pd.DataFrame({
      'A': [4,5,6,11,8, 22],
      'B': [5,6,7, 67, 2, 34],
      'C': [ "sat", "bat", "flat", "more", "data", "exp"],
     'ID': ['gxt15f', 'gxt0yl', 'gxszzn', 'get1jh', 'grt10e', 'gxt1ls']

    })

dataframe3 = pd.DataFrame({ 'A':[], 'B':[], 'C':[], 'ID':[] })

dataframe4 = pd.DataFrame({
    'ID': ['gxt1bd', 'gxt1f9', 'gxt10i', 'gxt15f', 'gxt0yl', 'gxszzn'],
    'things': ["cat", "bat", "mat", "doris", "flag", "jam"],
    'nums': [56,285,95, 455, 12, 46],
    'log': [True, False, False, True, True, False]
    })

dataframe_merged = pd.DataFrame.from_dict({'A': {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 11, 7: 8, 8: 22},
                                           'B': {0: 2, 1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 67, 7: 2, 8: 34},
                                           'C': {0: 'hat', 1: 'cat', 2: 'mat', 3: 'sat', 4: 'bat', 5: 'flat', 6: 'more', 7: 'data', 8: 'exp'},
                                           'ID': {0: 'gxt1bd', 1: 'gxt1f9', 2: 'gxt10i', 3: 'gxt15f', 4: 'gxt0yl', 5: 'gxszzn', 6: 'get1jh', 7: 'grt10e', 8: 'gxt1ls'}})

def test_merge_data_unique():
    assert_frame_equal(rd.merge_data_unique(dataframe1, dataframe2), dataframe_merged)
    assert_frame_equal(rd.merge_data_unique(dataframe1, dataframe3), dataframe1)
    assert_frame_equal(rd.merge_data_unique(dataframe3, dataframe1), dataframe1)
    assert_frame_equal(rd.merge_data_unique(dataframe1, dataframe1), dataframe1)


datastore = pd.DataFrame({
      'A': [1,2,3,4,5,6, 56,155],
      'B': [2,3,4,5,6,7, 57,199],
      'C': ["hat", "cat", "mat", "sat", "bat", "flat", "flan", "plan"],
     'id': ['gxt1bd', 'gxt1f9', 'gxt10i', 'gxt15f', 'gxt0yl', 'gxszzn', 'hcuwd4', 'hd4nl1']
     })

newData = pd.DataFrame({
      'A': [3,4,5,6, 56,155,4,6867],
      'B': [4,5,6,7, 57,199,987,9],
      'C': ["mat", "sat", "bat", "flat", "flan", "plan", "harry", "pop"],
     'id': ['gxt10i', 'gxt15f', 'gxt0yl', 'gxszzn', 'hcuwd4', 'hd4nl1', 'hcsxmq', 'hd4jx6']
     })

newdata_only = pd.DataFrame({
      'A': [4,6867],
      'B': [987,9],
      'C': ["harry", "pop"],
     'id': ['hcsxmq', 'hd4jx6']
     })

def test_data_to_add():
    assert_frame_equal(rd.data_to_add(newData, datastore), newdata_only)


