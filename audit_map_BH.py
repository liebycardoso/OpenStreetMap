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


OSMFILE = "C:/Nanodegree/MongoDb/Trab_final/map_BH.osm"
street_type_re = re.compile(r'^\b(?u)\w\S+\.?', re.IGNORECASE)
street_title_re = re.compile(r'\b\w+\.\w+?', re.IGNORECASE)


expected_street = ["Rua", "Avenida", "Beco", "Rodovia", "Expressa", u"Praça", "Anel", "Alameda"]

expected_city = ["Belo Horizonte", "Sarzedo", "Betim", "Santa Luzia", "Nova Lima", "Contagem", u"Ribeirão das Neves"]

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
            
mapping_city = {"Beo Horizonte" : "Belo Horizonte",
                "Bh" : "Belo Horizonte"}

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
        if street_type not in expected_street:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    """
    Para cada chave "K", verifica se é nome da rua

    Args:
        element: Um node do arquivo XML
    Returns:
        Retorna True ou False 
    """
    return (elem.attrib['k'] == "addr:street")

def is_city_name(elem):
    """
    Para cada chave "K", verifica se é nome de cidade

    Args:
        element: Um node do arquivo XML
    Returns:
        Retorna True ou False 
    """
    return (elem.attrib['k'] == "addr:city")
    
def is_postal_code(elem):
    """
    Para cada chave "K", verifica se é postal_code (CEP) 

    Args:
        element: Um node do arquivo XML
    Returns:
        Retorna True ou False 
    """
    return (elem.attrib['k'] == "postal_code")    

def update_postal_code(postalcode):   
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
    if postalcode.find("-"):
        postalcode = postalcode.replace("-","")
        
        
    print postalcode    
    return postalcode


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
        
        if street_type not in expected_street:
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
            name = name.replace(title,mapping[title])              
        
    return name

def update_city(city, mapping):   
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
    city = city.title()   
       
    if city not in expected_city:
        try:
            city = city.replace(city, mapping[city])
        except:
            
            if city.startswith("Belo"):
                city = city[0:13]
        
    return city

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
                    for st_type, ways in street_types.iteritems():
                        for name in ways:
                            better_name = update_street_type(name, mapping_street)
                            better_name = update_street_title(better_name, mapping_title)
                elif is_city_name(tag):
                    update_city(tag.attrib['v'], mapping_city)
                elif is_postal_code(tag):
                    update_postal_code(tag.attrib['v'])
                    
    osm_file.close()
    return street_types


def test():
    st_types = audit(OSMFILE)
    #pprint.pprint(dict(st_types))
          
if __name__ == '__main__':
    test()