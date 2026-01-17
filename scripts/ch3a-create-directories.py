import os

directories = ['data', 'raw-data', 'plots']

for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)