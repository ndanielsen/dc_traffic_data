
# coding: utf-8

# ## Loading Parking Violation Data and cleaning operations

# In[7]:

import glob
import json
import pandas as pd
import requests
import time
import os

# In[2]:



# In[3]:

with open('notebooks/dc_parking_violations.json', 'r') as f:
    parking_violations = json.load(f)


# In[ ]:

for fullname, csv in parking_violations.items():
    download_file =  csv + '.csv'
    local_filename = '_'.join(name.lower() for name in fullname.split() ) + '.csv'
    local_filename = './parkingdata/' + local_filename
    if not os.path.isfile(local_filename):
        #REQUESTED_TRUE = True
        #while REQUESTED_TRUE:
        time.sleep(5)
        r = requests.get(download_file)
        if not b'"status":"Processing","generating":{}' in r.content:
            with open(local_filename, 'wb') as f:
                f.write(r.content)
            print(local_filename)
        else:
            print('bad request: %s' % local_filename)
