import bdsutils

url = 'https://dati.lnb.lv/files/natl_bibliography-2014-2023-marc.zip'
target_file = target_dir + '/lnb-natl_bibliography-2014-2023-marc.zip'

download_and_unzip(url, target_file)

# os.rename(target_dir + '/data', target_dir + '/lnb')