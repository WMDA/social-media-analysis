import pandas as pd

import pandas_gbq

import requests

import io

import base64

import datetime



def cache_google_mobility_data(event, context):

    """

    Retrieves the mobility dataset from Google: https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv

    Database entries include date and time of backup.

    """



    # Decode pub/sub message

    message = base64.b64decode(event['data']).decode('utf-8')



    # set url to None by default or the message content if the message is not "trigger"

    url = None if message == "trigger" else message



    # Collect the data from url and add columns for date and time the data was collected

    current_data = collect_google_mobility(url)

    current_data["backup_date"] = datetime.date.today()

    current_data["backup_time"] = datetime.datetime.today().time()



    # Correctly format the column names for database storage

    current_data.columns = [col.lower().replace(" ", "_") for col in current_data.columns]

    pandas_gbq.to_gbq(current_data, "covid19_datastore.google_mobility", project_id="bpi-covid19", if_exists="append")

    return None





def collect_google_mobility(url = None):

    if url is None:

        url = "https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv?cachebust=a88b56a24e1a1e25"



    datastr = requests.get(url,allow_redirects=True).text

    data_file = io.StringIO(datastr)

    mobility_table = pd.read_csv(data_file, low_memory=False)



    return mobility_table
