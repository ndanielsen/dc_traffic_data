import os
import sys
import zipfile
import requests

from clint.textui import progress

parking_file_zip = 'vz-hackathon+2.zip'
data_folder = 'vz-hackathon'

raw = True if 'raw' in sys.argv else False
clean = True if 'clean' in sys.argv else False
small_geojson = True if 'small_geojson' in sys.argv else False

def download_unzip(url, datafile, data_folder):
    if not os.path.isfile(datafile):
        print('Warning, this might take awhile dependin on your internet connection')
        with open(datafile, 'wb') as handle:
            response = requests.get(url, stream=True)
            if not response.ok:
                print('ERROR')
            print('Downloading %s' % datafile)
            total_length = int(response.headers.get('content-length')) / 1024 + 1
            for block in progress.bar(response.iter_content(1024), expected_size=total_length):
                handle.write(block)
                handle.flush()
    if not os.path.isdir(data_folder):
        print('Unzipping %s File' % datafile)
        with zipfile.ZipFile(datafile,"r") as zip_ref:
            zip_ref.extractall()

if raw:
    url = 'https://s3.amazonaws.com/dctraffic/vz-hackathon+2.zip'
    file_zip = 'vz-hackathon+2.zip'
    data_folder = 'vz-hackathon'
    download_unzip(url, file_zip, data_folder)

if clean:
    url = 'https://s3.amazonaws.com/dctraffic/traffic.zip'
    file_zip = 'traffic.zip'
    data_folder = 'traffic'
    download_unzip(url, file_zip, data_folder)

if small_geojson:
    url = 'https://s3.amazonaws.com/dctraffic/data.zip'
    file_zip = 'data.zip'
    data_folder = 'data'
    download_unzip(url, file_zip, data_folder)
