# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 21:05:47 2016

@author: MasterLieby
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.cElementTree as ET
import pprint
import re
import json
import codecs

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
tag_problematica = []

def key_type(element, keys):
    """
    Para cada chave "K", verifica e conta o total de caracteres problemáticos, minúsculos  e outros.
    Imprime as tags com caracteres problemáticos.

    Args:
        element: Um node do arquivo XML
        keys: Dicionário a ser preenchido
    Returns:
        Retorna um dicionário com o total de tags com caracteres minúsculos, 
        minúsculos com :, problemáticos e todos os outros.
    """
    
    
    if element.tag == "tag":
        k = element.attrib['k'] 
        if lower.search(k):
            keys['lower'] +=1  
        elif lower_colon.search(k):
            keys['lower_colon']+=1
        elif problemchars.search(k):
            keys['problemchars'] +=1
            tag_problematica.append(k)            
        else: 
            keys['other']+=1            
        
    return keys

def process_map(filename):
    """
    Cria o dicionário Keys com as chaves para identificar o total de tags em cada situação.
    Percorre todo o arquivo XML, chamando a função Key_type para cada node da estrutura de dados.

    Args:
        filename: nome do arquivo a ser processado.
    Returns:
        Retorna um dicionário com o total de tags com caracteres minúsculos, 
        minúsculos com :, problemáticos e todos os outros.
    """
    
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    tags = {}
    tags_child = {}
    with codecs.open('C:/Nanodegree/MongoDb/Trab_final/Summary_OSM_BH.json', "w") as fo:
        for _, element in ET.iterparse(filename):
            keys = key_type(element, keys)
            tags = count_tags(element, tags)
            tags_child = count_child_tags(element, tags_child)
        fo.write(json.dumps(keys) + "\n")
        fo.write(json.dumps(tags) + "\n")
        fo.write(json.dumps(tags_child, indent=2) + "\n")

def count_tags(element, keys):
        # YOUR CODE HERE
    if element.tag in keys:
        keys[element.tag] += 1
    else:
        keys[element.tag] = 1
    return keys

def count_child_tags(element, keys):
    
    if element.tag == "node" or element.tag == "way":
        for tag in element.iter("tag"):
            if tag.attrib['k'] in keys:
                keys[tag.attrib['k']] += 1
            else:
                keys[tag.attrib['k']] = 1
    return keys

def test():
    process_map('C:/Nanodegree/MongoDb/Trab_final/map_BH.osm')
        

if __name__ == "__main__":
    test()