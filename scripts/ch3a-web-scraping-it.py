import requests
import lxml.html
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
    doc = lxml.html.fromstring(content)
    extract_translations(doc)
    from_param = extract_next_link(doc)
    if from_param != None:
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
    return None

def extract_translations(doc):
    global record_counter, authors, translators
    items = doc.findall('body/table[@class="restable"]/tr/td[@class="res2"]', {})
    for item in items:
        record_counter += 1
        record = {'id': record_counter}
        spans = item.findall('span')
        for span in spans:
            key = span.get('class')
            if key == 'sn_pub':
                subs = span.findall('span')
                for sub in subs:
                    extract_key_value(record, sub)
            else:
                extract_key_value(record, span)
        record, author, translator = normalize_record(record)
        records.append(record)
        authors += author
        translators += translator

def extract_key_value(record, span):
    key = re.sub(r'^sn_', '', span.get('class'))
    if key not in ['auth_name', 'auth_firstname', 'transl_name', 'transl_firstname']:
        field_names.update([key])
    if key not in record:
        record[key] = []
    record[key].append(span.text)

def normalize_record(record):
    for key, value in record.items():
        if key not in ['id', 'auth_name', 'auth_firstname', 'transl_name', 'transl_firstname']:
            record[key] = ', '.join(value)

    authors = extract_names(record, 'auth_name', 'auth_firstname')
    translators = extract_names(record, 'transl_name', 'transl_firstname')

    for key, value in record.items():
        if isinstance(value, list) and len(value) > 1:
            multivalue_keys.update([key])

    return record, authors, translators

def extract_names(record, namekey, firstnamekey):
    name_records = []
    i = -1
    if namekey in record:
        firstnames = record.get(firstnamekey, [])
        for name in record.get(namekey):
            name_record = {'rid': record['id'], 'last': name, 'first': None}
            if name != 'et al.':
                i += 1
                if (len(firstnames) > i):
                    name_record['first'] = firstnames[i]
            name_records.append(name_record)
        del record[namekey]
        if len(firstnames) > 0:
            del record[firstnamekey]
    
    return name_records

cache_dir = 'cache'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

record_counter = 1
records = []
authors = []
translators = []
field_names = Counter({})
multivalue_keys = Counter()

request_page(it_params)

output_dir = os.path.join('raw-data', 'it')
create_dir(output_dir)

with open(os.path.join(output_dir, 'it.csv'), 'w', encoding='utf-8') as csv_file:
    column_names = ['id'] + list(field_names.keys())
    output_writer = csv.DictWriter(csv_file, fieldnames=column_names)
    output_writer.writeheader()
    output_writer.writerows(records)

with open(os.path.join(output_dir, 'authors.csv'), 'w', encoding='utf-8') as csv_file:
    output_writer = csv.DictWriter(csv_file, fieldnames=['rid', 'last', 'first'])
    output_writer.writeheader()
    output_writer.writerows(authors)

with open(os.path.join(output_dir, 'translators.csv'), 'w', encoding='utf-8') as csv_file:
    output_writer = csv.DictWriter(csv_file, fieldnames=['rid', 'last', 'first'])
    output_writer.writeheader()
    output_writer.writerows(translators)
