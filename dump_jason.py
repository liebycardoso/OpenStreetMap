#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 17:05:47 2016

@author: MasterLieby
"""



import xml.etree.cElementTree as ET
import re
import codecs
import json
import unicodedata
import audit_map_BH
from collections import defaultdict

"""
{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
POSICAO = ["lat", "lon"]
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

    
def remove_accentuation(string):
    string = unicodedata.normalize('NFD', string)
    return u''.join(ch for ch in string if unicodedata.category(ch) != 'Mn')


def shape_element(element):
    node = {}
    address = {}
    node_refs = []
    pos = [None, None]
    created = {}
    street_types = defaultdict(set)
    street_types_dic = defaultdict(set)
    
    if element.tag == "node" or element.tag == "way" :
        
        # Trabalha com elementos em primeiro nível
        for atributo in element.attrib.keys():
            
            if atributo in CREATED:                
                if type(element.attrib[atributo]) == type(u'/'):
                    #created[atributo] = unicodedata.normalize('NFD',x.encode('utf-8').decode('utf8'))
                    created[atributo] = remove_accentuation(element.attrib[atributo])
                else:
                    created[atributo] = element.attrib[atributo]
            
            #if atributo in POSICAO:
                #pos[0] = float(element.attrib["lat"])
                #pos[1] = float(element.attrib["lon"])
                
            if 'lat' in atributo:
                node['pos'] = [float(element.attrib['lat']), float(element.attrib['lon'])]    
            
            if re.search(problemchars, element.attrib[atributo]):
                continue
                
        for elemento in element:
            
            # Se a linha tem a tag nd, agrupa todos os ref em um array
            #for nd in element.iter("nd"):               
            if elemento.tag == "nd":
                if elemento.attrib['ref']:
                    node_refs.append(elemento.attrib['ref'])
 
#---------------------------------------------------------
                       
                # Se a linha tem a tag tag, agrupa todos os valores de v em k
        for tag in element.iter("tag"):
            key = tag.attrib['k']
            if key:
                if key.count(':') > 1:
                    pass
                if key.startswith("addr"):
                    if key.count(':') == 1: 
                        keyAddress = key.split(":")[1]
                        if audit_map_BH.is_street_name(tag):
                            #street_types = audit_map_BH.audit_street_type(street_types_dic, tag.get('v'),expected_street)
                            #for st_type, ways in street_types.iteritems():
                                #for name in ways:
                            better_name = audit_map_BH.update_street_type(tag.get('v'), mapping_street,expected_street)
                            street_name = audit_map_BH.update_street_title(better_name, mapping_title)
                            address[keyAddress] = street_name
                        elif audit_map_BH.is_city_name(tag):
                            address[keyAddress] = audit_map_BH.update_city(tag.get('v'), mapping_city)
                        elif audit_map_BH.is_postal_code(tag):
                            address[keyAddress] = audit_map_BH.update_postal_code(tag.get('v'))
                        else:
                            keyAddress = key.split(":")[1]
                            address[keyAddress] = tag.get('v') 
                            
                else:
                    node[key] = tag.get('v') 
                    
       
            '''
            if audit_map_BH.is_city_name(tag):
                node[key] = audit_map_BH.update_city(tag.get('v'), mapping_city)
            elif audit_map_BH.is_postal_code(tag):
                node[key] = audit_map_BH.update_postal_code(tag.get('v'))
            '''                
#---------------------------------------------------------------------                            
                        
                    
        node['type'] = element.tag
        node['id'] = element.attrib['id']
        try:
            node['visible'] = element.attrib['visible'] 
        except:
            pass
        
        
                        
        if created:
            node['created']=created  
        #if pos:
            #node['pos']= pos
        if address:
            node["address"] = address
        if node_refs:    
            node["node_refs"] = node_refs
        node_refs = []
        address = {}
        #if node:
            #print node 
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                print el
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

def test():
    data = process_map("C:/Nanodegree/MongoDb/Trab_final/sample_BH.osm", True)

if __name__ == "__main__":
    test()