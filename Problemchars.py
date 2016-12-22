# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 15:03:23 2016

@author: MasterLieby
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
  "lower", for tags that contain only lowercase letters and are valid,
  "lower_colon", for otherwise valid tags with a colon in their names,
  "problemchars", for tags with problematic characters, and
  "other", for other tags that do not fall into the other three categories.
"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        k = element.attrib['k'] 
        if lower.search(k):
            keys['lower'] +=1  
        elif lower_colon.search(k):
            keys['lower_colon']+=1
        elif problemchars.search(k):
            keys['problemchars'] +=1
            print k
        else: 
            keys['other']+=1
        
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertion below will be incorrect then.
    # Note as well that the test function here is only used in the Test Run;
    # when you submit, your code will be checked against a different dataset.
    keys = process_map('C:/Nanodegree/MongoDb/Trab_final/sample_BH.osm')
    pprint.pprint(keys)
    
if __name__ == "__main__":
    test()