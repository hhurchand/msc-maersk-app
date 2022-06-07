import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime
import re
import os
import streamlit as st

import json
import re
import requests
import feedparser


st.header("ETA APP")
shipping_company = st.radio(label = 'Select one of', options = ['MSC','MAERSK'])


container_id = st.text_input("CONTAINER NUMBER")


if shipping_company == "MAERSK":

    response = requests.get("https://api.maerskline.com/track/{}?operator=maeu".format(container_id))
    json_content = response.json()

    dict_maersk = {feature:list() for feature in ['Terminal','Activity','Actual time','Expected time']}
    for entry in json_content['containers'][0]['locations']:

        try:
            dict_maersk['Terminal'].append(entry['terminal'])
        except:
            dict_maersk['Terminal'].append('Not found')

        try:
            dict_maersk['Activity'].append(entry['events'][0]['activity'])
        except:
            dict_maersk['Activity'].append('Not found')

        try:
            actual_time = entry['events'][0]['actual_time'] 
            dict_maersk['Actual time'].append(actual_time[0:10])
        except:
            dict_maersk['Actual time'].append("NA")

        try:
            expected_time = entry['events'][0]['expected_time'] 
            dict_maersk['Expected time'].append(expected_time[0:10])
        except:
            dict_maersk['Expected time'].append("NA")


        df = pd.DataFrame(dict_maersk)
        st.write(df)

        st.write("ETA in Montreal - if known:\n",json_content['containers'][0]['eta_final_delivery'][0:10])
        

elif shipping_company == "MSC":
        url = \
        "https://wcf.mscgva.ch/publicasmx/Tracking.asmx/GetRSSTrackingByContainerNumber?ContainerNumber={}".format(container_id)
        
        d = feedparser.parse(url)
        df_table = {feature:list() for feature in ["title","location","Description","Date"]}
        for entry in d["entries"]:
            try:
                description = entry.get("description")
                description_list = re.findall("</td><td>(.*?)</td>",description)
            except:
                description_list = ["NA"]
            try:
                date_list = re.findall("</td><td>\n(.*?)\n\t </td>",description)
                if len(date_list) == 0:
                    date_list = ["NA"]  
            except:
                date_list = ["NA"]

            df_table["title"].append(entry.get("title"))
            df_table["location"].append(description_list[0])
            df_table["Description"].append(description_list[1])
            df_table["Date"].append(date_list[0])
        df_table = pd.DataFrame(df_table)
        st.write(df_table)
