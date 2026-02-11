import urllib.request
import zipfile
import os

target_dir = 'raw-data'

def download_and_unzip(url, target_file):
    """
    Download a zip file, and uncompress it
    
    Parameters
    ----------
    url : str
        The URL of the zip file to download
    sound : str
        The local file name
    """

    urllib.request.urlretrieve(url, target_file)

    with zipfile.ZipFile(target_file, 'r') as zip_ref:
        zip_ref.extractall(target_dir)

def create_dir(dir):
    """
    Create a directory if it doesn't yet exist
    
    :param dir: the directory name
    """
    if not os.path.exists(dir):
        os.makedirs(dir)
