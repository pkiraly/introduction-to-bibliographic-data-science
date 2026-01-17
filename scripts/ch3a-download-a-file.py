import urllib.request
import zipfile

urllib.request.urlretrieve(
    "https://dati.lnb.lv/files/natl_bibliography-2014-2023-marc.zip",
    "raw-data/lnb-natl_bibliography-2014-2023-marc.zip")

with zipfile.ZipFile('raw-data/lnb-natl_bibliography-2014-2023-marc.zip', 'r') as zip_ref:
    zip_ref.extractall('raw-data')
