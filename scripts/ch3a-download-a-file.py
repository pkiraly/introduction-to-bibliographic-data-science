import urllib.request
import zipfile
import os

url = 'https://dati.lnb.lv/files/natl_bibliography-2014-2023-marc.zip'
target_dir = 'raw-data'
target_file = target_dir + '/lnb-natl_bibliography-2014-2023-marc.zip'

urllib.request.urlretrieve(url, target_file)

with zipfile.ZipFile(target_file, 'r') as zip_ref:
    zip_ref.extractall(target_dir)

os.rename(target_dir + '/data', target_dir + '/lnb')