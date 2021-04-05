# Set linting rules
# pylint: disable=undefined-variable

import re
import urllib.request
import xml.etree.ElementTree as ET

file_path = "{}/weather.xml".format(temp_directory)
location = config['weather']['location']
unit = config['weather']['unit'].upper()

url = "https://weather-broker-cdn.api.bbci.co.uk/en/observation/rss/{}".format(
    location)

# Download File
urllib.request.urlretrieve(url, file_path)

# Parse xml
xml = ET.parse(file_path).getroot()

# Get weather description from xml
for tag in xml[0]:
    if tag.tag == 'item':
        for t in tag:
            if t.tag == 'description':
                weather = t.text

regex = '\\d+.[C|F]'
t = re.findall(regex, weather)

if unit == 'C':
    temp = t[0]
elif unit == 'F':
    temp = t[1]

print('Processed weather information. Temperature currently is: {}'.format(temp))
