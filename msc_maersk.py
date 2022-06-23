#!/usr/bin/env python
# coding: utf-8

# In[1]:


#%%writefile msc_maersk.py
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
shipping_company = st.radio(label = 'Select one of', options = ['MSC','MAERSK','HAPAG'])



with st.form(key="my_form"):

    if shipping_company == "MAERSK":
        container_id = st.text_input("CONTAINER NUMBER")

        if container_id == "":
            dict_maersk = {feature:list() for feature in ['Terminal','Activity','Actual time','Expected time']}
            df = pd.DataFrame(dict_maersk)
        else:
            response = requests.get("https://api.maerskline.com/track/{}?operator=maeu".format(container_id))
            json_content = response.json()

            dict_maersk = {feature:list() for feature in ['Terminal','Activity','Actual time','Expected time']}
            df = pd.DataFrame(dict_maersk)

            try:
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
            except:
                st.write("Please verify the container id. It may be too old or invalid")
        submit_button = st.form_submit_button(label='Submit Maersk')
    elif shipping_company == "MSC":
            container_id = st.text_input("CONTAINER NUMBER")
            url =             "https://wcf.mscgva.ch/publicasmx/Tracking.asmx/GetRSSTrackingByContainerNumber?ContainerNumber={}".format(container_id)

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
            submit_button = st.form_submit_button(label='Submit MSC')
    elif shipping_company == "HAPAG":
            st.write("ENTER UP TO THREE HAPAG CONTAINER NUMBERS")
            st.write("UPDATED CONTAINER INFO WILL BE SENT TO THE GIVEN EMAIL")

            container_id_1 = st.text_input("CONTAINER NUMBER 1")
            container_id_2 = st.text_input("CONTAINER NUMBER 2")
            container_id_3 = st.text_input("CONTAINER NUMBER 3")
            email = st.text_input("Email")

            concat_ids= container_id_1 + ";" + container_id_2 + ";" + container_id_3
            container_ids=concat_ids.strip(';')
            subject_line = """ "T: """ + container_ids + """\"""" 
            email = """\"""" + email + """\""""  
            a = """ curl "https://api.postmarkapp.com/email" """
            b = """ -X POST """
            c = """ -H "Accept: application/json" """
            d = """ -H "Content-Type: application/json" """
            e = """ -H "X-Postmark-Server-Token: 13b13028-020e-49d8-9470-27ed2dece0ab" """
            f = """ -d \' { """
            g = f""" "From": {email},
                     "To": "getinfo@hlag.com",
                     "Subject": {subject_line},
                     "TextBody": " ",
                     "MessageStream": "outbound" """
            h =  """    }\' """

            cmd = a+b+c+d+e+f+g+h
#            st.write(subject_line)
            st.write(email)
#            st.write(cmd)
            os.system(cmd)
            submit_button = st.form_submit_button(label='Submit Hapag')

