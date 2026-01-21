import urllib.request
import zipfile
import os

target_dir = 'raw-data'

def download_and_unzip(url, target_file):

    urllib.request.urlretrieve(url, target_file)

    with zipfile.ZipFile(target_file, 'r') as zip_ref:
        zip_ref.extractall(target_dir)

# os.rename(target_dir + '/data', target_dir + '/lnb')