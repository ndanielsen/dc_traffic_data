import os
import zipfile
import requests


parking_file_zip = 'vz-hackathon+2.zip'

if not os.path.isfile(parking_file_zip):

    print('Warning, this might take awhile dependin on your internet connection')

    with open(parking_file_zip, 'wb') as handle:
        response = requests.get('https://s3.amazonaws.com/dctraffic/vz-hackathon+2.zip', stream=True)

        if not response.ok:
            # Something went wrong
            print('ERROR')

        for block in response.iter_content(1024):

            handle.write(block)
