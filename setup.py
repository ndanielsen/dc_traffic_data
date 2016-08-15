import os
import sys
import zipfile
import requests

from clint.textui import progress

# commandline args
raw = True if 'raw' in sys.argv else False
# clean = True if 'clean' in sys.argv else False
small_geojson = True if 'small_geojson' in sys.argv else False
parking_1million = True if 'parking_1million' in sys.argv else False
parking_100k = True if 'parking_100k' in sys.argv else False
cleaned_parking_data = True if 'cleaned_parking_data' in sys.argv else False

def download(url, datafile):
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

def unzip(datafile, data_folder):
    if not os.path.isdir(data_folder):
        print('Unzipping %s File' % datafile)
        with zipfile.ZipFile(datafile,"r") as zip_ref:
            zip_ref.extractall()
        print('Extracted to: %s', data_folder)

def unzip_to_dir(datafile, data_folder):
    print('Unzipping %s File' % datafile)
    with zipfile.ZipFile(datafile,"r") as zip_ref:
        zip_ref.extractall(data_folder)
    print('Extracted to: %s', data_folder)

if raw:
    url = 'https://s3.amazonaws.com/dctraffic/vz-hackathon+2.zip'
    file_zip = 'vz-hackathon+2.zip'
    data_folder = 'vz-hackathon'
    download(url, file_zip)
    unzip(file_zip, data_folder)

# if clean:
#     url = 'https://s3.amazonaws.com/dctraffic/traffic.zip'
#     file_zip = 'traffic.zip'
#     data_folder = 'traffic'
#     download(url, file_zip)
#     unzip(file_zip, data_folder)

if small_geojson:
    url = 'https://s3.amazonaws.com/dctraffic/data.zip'
    file_zip = 'data.zip'
    data_folder = 'data'
    download(url, file_zip)
    unzip(file_zip, data_folder)

if parking_1million:
    url = "https://s3.amazonaws.com/dctraffic/clean_parking_violations_1million_sample.csv.zip"
    file_zip = "clean_parking_violations_1million_sample.csv.zip"
    data_folder = 'sampled_data'
    download(url, file_zip)
    unzip_to_dir(file_zip, data_folder)

if parking_100k:
    url = "https://s3.amazonaws.com/dctraffic/clean_parking_violations_100k_sample.csv.zip"
    file_zip = "clean_parking_violations_100k_sample.csv.zip"
    data_folder = 'sampled_data'
    download(url, file_zip)
    unzip_to_dir(file_zip, data_folder)

if cleaned_parking_data:
    url = "https://s3.amazonaws.com/dctraffic/clean_parking_violations.csv.zip"
    file_zip = "clean_parking_violations.csv.zip"
    data_folder = 'cleaned_data'
    download(url, file_zip)
    unzip_to_dir(file_zip, data_folder)
