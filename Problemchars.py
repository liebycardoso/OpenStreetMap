#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 15:03:23 2016

@author: MasterLieby
"""

import xml.etree.cElementTree as ET
import pprint
import re
"""
  "lower" => tags com letras minúsculas
  "lower_colon" => tags que tem dois pontos
  "problemchars" => Caracteres problemáticos, inclusive newline, return e tab
  "other" => Todos caracteres que não foram enquadrados acima
"""


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
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

def test():
    
    keys = process_map('C:/Nanodegree/MongoDb/Trab_final/map_BH.osm')
    pprint.pprint(keys)
    pprint.pprint(tag_problematica)
    
if __name__ == "__main__":
    test()