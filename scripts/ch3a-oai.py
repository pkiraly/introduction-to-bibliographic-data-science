import io
import sys
import os
from lxml import etree
from sickle import Sickle

if len(sys.argv) == 1:
    print('Please give a directory name')
    exit()
dir = sys.argv[1]
if not os.path.exists(dir):
    os.mkdir(dir)
print('saving to %s' % (dir))

namespaces = {
    'oai': 'http://www.openarchives.org/OAI/2.0/',
    'marc21': 'http://www.loc.gov/MARC21/slim'
}

header = '<?xml version="1.0" encoding="utf8"?>' + "\n" + '<collection>' + "\n"
footer = '</collection>'

def write_output(output, file_counter, dir):
    """Writes MARC records to file"""
    file_name = "%s/%06d.xml" % (dir, file_counter)
    print(file_name)
    with io.open(file_name, 'w', encoding='utf8') as f:
        f.write(header)
        f.write("\n".join(output) + "\n")
        f.write(footer)

xmlrecords = []
file_counteri = 0
record_count = 0

sickle = Sickle('https://data.digar.ee/repox/OAIHandler', max_retries=4)
it = sickle.ListRecords(metadataPrefix='marc21xml', set='erb')
for record in it:
    tree = etree.ElementTree(record.xml)
    token = tree.xpath('/resumptionToken', namespaces=namespaces)

    records = tree.xpath('/oai:record[*]/oai:metadata/marc21:record', namespaces=namespaces)
    for rec in records:
        xmlrecord = etree\
               .tostring(rec, encoding='utf8', method='xml')\
               .decode("utf-8")\
               .replace("<?xml version='1.0' encoding='utf8'?>\n", '')
        xmlrecords.append(xmlrecord)
        record_count += 1
    if len(xmlrecords) >= 100000:
        write_output(xmlrecords, file_counter, dir)
        xmlrecords = []
        file_counter += 1

if len(xmlrecords) > 0:
    write_output(xmlrecords, file_counter, dir)

print('saved %d records to %d files' % (record_count, file_counter))

