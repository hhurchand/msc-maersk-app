#!/usr/bin/env python
# coding: utf-8

# In[26]:


#!pip install streamlit


# In[27]:


import pandas as pd
import pyexasol
from dateutil.relativedelta import relativedelta
from datetime import datetime
import re
import os
import streamlit as st


# In[28]:


import json
import re
import requests


# In[29]:


import feedparser


# In[30]:

container_id = st.text_input("CONTAINER NUMBER")
st.write(container_id)
response = requests.get("https://api.maerskline.com/track/{}?operator=maeu".format(container_id))


# In[31]:


json_content = response.json()


# In[32]:


dict_maersk = {feature:list() for feature in ['terminal','activity','date','expected']}
for entry in json_content['containers'][0]['locations']:
#    dict_maersk['terminal'].append(entry['terminal'])
#    dict_maersk['activity'].append(entry['terminal']['events'][0])
    dict_maersk['terminal'].append(entry['terminal'])
    dict_maersk['activity'].append(entry['events'][0]['activity'])
    try:
        dict_maersk['date'].append(entry['events'][0]['actual_time'])
    except:
        dict_maersk['date'].append("NA")
    try:
        dict_maersk['expected'].append(entry['events'][0]['expected_time'])
    except:
        dict_maersk['expected'].append("NA")


# In[33]:


df = pd.DataFrame(dict_maersk)



# In[34]:


#!pip install pipreqs


# In[35]:


st.write(df)


# In[ ]:





# In[ ]:




