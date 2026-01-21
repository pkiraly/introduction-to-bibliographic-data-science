from bdsutils import target_dir, download_and_unzip

url = 'https://fbtee.uws.edu.au/stn/database/download/STN_database.zip'
target_file = target_dir + '/stn_database.zip'

download_and_unzip(url, target_file)

# os.rename(target_dir + '/data', target_dir + '/lnb')