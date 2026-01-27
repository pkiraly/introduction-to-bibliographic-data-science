import requests
import lxml.html
import lxml.etree as etree
import os
import re
import urllib.parse
import csv
from collections import Counter

base_url = 'https://www.unesco.org/xtrans/bsresult.aspx'
it_params = {
    'a': 'Bourdieu, Pierre',
    'fr': 0
}

cache_dir = 'cache'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

def request_page(it_params):
    cache_file = os.path.join(cache_dir, f'results_{it_params['fr']}.html')
    print(cache_file)
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            content = f.read()
        process_page(content)
    else:
        response = requests.get(base_url, params=it_params)
        if response.status_code == 200:
            content = response.text
            if re.search('The requested URL was rejected.', content) is None:
                with open(cache_file, 'wb') as f:
                    f.write(response.content)
            process_page(content)

def process_page(content):
    # print(content)
    doc = lxml.html.fromstring(content)
    extract_translations(doc)
    from_param = extract_next_link(doc)
    if from_param != '':
        it_params['fr'] = from_param
        request_page(it_params)

def extract_next_link(doc):
    next = doc.findall('body/table[@class="nav"]/tr[1]/td[@class="next"]/a', {})
    if len(next) > 0:
        link = next[0].get('href')
        parsed_link = urllib.parse.urlparse(link)
        parameters = urllib.parse.parse_qs(parsed_link.query)
        if 'fr' in parameters and len(parameters['fr']) == 1:
            return parameters['fr'][0]
    return ''

def extract_translations(doc):
    items = doc.findall('body/table[@class="restable"]/tr/td[@class="res2"]', {})
    for item in items:
        record = {}
        spans = item.findall('span')
        for span in spans:
            key = span.get('class')
            if key == 'sn_pub':
                subs = span.findall('span')
                for sub in subs:
                    extract_key_value(record, sub)
            else:
                extract_key_value(record, span)
        records.append(record)

def extract_key_value(record, span):
    key = re.sub(r'^sn_', '', span.get('class'))
    field_names.update([key])
    if key not in record:
        record[key] = []
    record[key].append(span.text)

records = []
field_names = Counter({})
request_page(it_params)
print(field_names)
field_names.keys()

output_dir = 'raw-data/it'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
with open(output_dir + '/it.csv', 'w', encoding='utf-8') as csv_file:
    output_writer = csv.DictWriter(csv_file, fieldnames=field_names.keys())
    output_writer.writeheader()
    output_writer.writerows(records)