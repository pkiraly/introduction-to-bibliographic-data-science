from bdsutils import target_dir, download_and_unzip
import os

url = 'https://fbtee.uws.edu.au/stn/database/download/STN_database.zip'
target_file = target_dir + '/stn_database.zip'

download_and_unzip(url, target_file)

directory = target_dir + '/fbtee'
if not os.path.exists(directory):
    os.mkdir(directory)

os.rename(target_dir + '/chop_leeds_ac_uk.sql', directory + '/chop_leeds_ac_uk.sql')