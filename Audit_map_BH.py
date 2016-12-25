#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 16:32:07 2016

@author: MasterLieby
"""

"""

"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "C:/Nanodegree/MongoDb/Trab_final/map_BH.osm"
street_type_re = re.compile(r'^\b(?u)\w\S+\.?', re.IGNORECASE)
street_title_re = re.compile(r'\b\w+\.\w+?', re.IGNORECASE)


expected = ["Rua", "Avenida", "Beco", "Rodovia", "Expressa", u"Praça", "Anel", "Alameda"]


mapping_street = { "Av.": "Avenida",
                "Av": "Avenida",
                "Rod.": "Rodovia",
                "Al.": "Alameda",
                "R.": "Rua",
                u"Anél": "Anel",
                "R.B" : "Rua B",
                "Pc" : u"Praça", 
                "Avendia" : "Avenida",
                "Alamedas" : "Alameda",
                "Av.Afonso" : "Avenida Afonso",
                "Eua": "Rua"
                }

mapping_title = {'Prof.': u'Professor',
                 'Dr.': u"Doutor"
            }

def audit_street_type(street_types, street_name):
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
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
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
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
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
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_street_type(name, mapping):
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
    name = name.title()
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        
        if street_type not in expected:
            try:
                name = re.sub(street_type_re, mapping_street[street_type], name)
            except:
                
                name = "Rua " + name  
                
    return name

def update_street_title(name, mapping):   
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
    title = name.split()[1]
    
    if title.endswith("."):
        if mapping_title[title]:
            name = name.replace(title,mapping_title[title])
               
        
    return name


def test():
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_street_type(name, mapping_street)
            better_name = update_street_title(better_name, mapping_title)
            print name, "=>", better_name
           
if __name__ == '__main__':
    test()