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
"""
Modelo do dicionário esperado após execução do método shape_element(element)
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

problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
NODE = ["id","visible","amenity","cuisine","name","phone"]

expected_street = ["Rua", "Avenida", "Beco", "Rodovia", "Expressa", u"Praça", "Anel", "Alameda"]
expected_city = ["Belo Horizonte", "Sarzedo", "Betim", "Santa Luzia", "Nova Lima", "Contagem", u"Ribeirão das Neves"]


mapping_street = {  "Av.": "Avenida",
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
                "Bh" : "Belo Horizonte"
               }

    
def remove_accentuation(txt):
    """
    Recebe um texto, normaliza, retirando os caracteres unicode

    Args:
        txt: Texto a ser modificado
    Returns:
        Versão do texto sem os caracteres unicode
    """    
    txt = unicodedata.normalize('NFD', txt)
    return u''.join(ch for ch in txt if unicodedata.category(ch) != 'Mn')


def shape_element(element):
    """
    Recebe um dos nós do arquivo XML, percorre todo o registro identificando
    a chave (k) e o valor associado (v).
    As chaves selecionadas para manipulação estão referenciadas nos arrays CREATED e NODE
    Os atributos que compõe o endereço são mapeados e corrigidos quando necessário.
    A versão adequada dos atributos é gravada no dicionário node

    Args:
        element: Representa um nó do arquivo XML
    Returns:
        node: Dicionário com os registros configurados
    """
    node = {}
    address = {}
    node_refs = []
    created = {}
    
    if element.tag == "node" or element.tag == "way" :
        # Recebe o tipo da tag [node, way]
        node['type'] = element.tag
        
        # Trabalha com elementos em primeiro nível
        for atributo in element.attrib.keys():
            
            # Se a chave está no array CREATED incluí a chave:atributo no dicionario created
            if atributo in CREATED:  
                # Verifica se o elemento retornado é unicode , se for remove os caracteres especiais
                if type(element.attrib[atributo]) == type(u'/'):                    
                    created[atributo] = remove_accentuation(element.attrib[atributo])
                else:
                    created[atributo] = element.attrib[atributo]
                    
            # Se a chave está no array NODE incluí a chave:atributo no dicionario node
            if atributo in NODE:
                node[atributo] = element.attrib[atributo]
             
            # Verifica a existencia da chave lat antes de atribuir valor à chave pos[lat,lon] 
            if 'lat' in atributo:
                node['pos'] = [float(element.attrib['lat']), float(element.attrib['lon'])]    
            
            # Se encontrado caracteres problemático, segue sem armazenar o valor            
            if re.search(problemchars, element.attrib[atributo]):
                continue
                
        
        for elemento in element:            
            # Se a linha tem a tag nd, agrupa todos os ref em um array                           
            if elemento.tag == "nd":
                if elemento.attrib['ref']:
                    node_refs.append(elemento.attrib['ref'])
 
                       
        # Se a linha tem a tag "tag", percorre item a item do componente e providencia as atualizações
        for tag in element.iter("tag"):
            # key recebe a chave - nome do atibuto
            key = tag.attrib['k']
            if key:
                '''
                Se a chave tem mais de :, o registro é ignorado. Esta é uma escolha de programação
                porque foi optado por não trabalhar com os registros com dois níveis de detalhe
                '''
                if key.count(':') > 1:
                    pass
                # Se a chave tem um identificador de endereço:
                if key.startswith("addr"):
                    if key.count(':') == 1: 
                        # KeyAddress recebe a string depois do ponto, porque ela indica se é nome da rua numero CEP
                        keyAddress = key.split(":")[1]
                        # Verifica se é nome de rua
                        if audit_map_BH.is_street_name(tag):
                            # Corrige o nome da cidade
                            better_name = audit_map_BH.update_street_type(tag.get('v'), mapping_street,expected_street)
                            # Substitui títulos abreviados por sua versão extendida
                            street_name = audit_map_BH.update_street_title(better_name, mapping_title)
                            address[keyAddress] = street_name
                        # verifica se é nome de cidade    
                        elif audit_map_BH.is_city_name(tag):
                            # Corrige o nome da cidade e atribuí o valor ao dicionário address
                            address[keyAddress] = audit_map_BH.update_city(tag.get('v'), mapping_city, expected_city)
                        # Verifica se é código postal (CEP)
                        elif audit_map_BH.is_postal_code(tag):
                            # Corrige o código do CEP somente númericos e atribuí o valor ao dicionário address
                            address[keyAddress] = audit_map_BH.update_postal_code(tag.get('v'))
                        else:
                            # Adiciona todos os outros atributos sem tratamento do valor
                            keyAddress = key.split(":")[1]
                            address[keyAddress] = tag.get('v') 
                            
                else:
                    # Adiciona todos os outros atributos que não compõe o endereço 
                    node[key] = tag.get('v').title() 
        
        # Grava os objetos temporários no dicionário final                
        if created:
            node['created']=created 
        if address:
            node["address"] = address
        if node_refs:    
            node["node_refs"] = node_refs
        node_refs = []
        address = {}
        
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    """
    Percorre cada elemento do arquivo OSM e para cada elemento chama shape_element() 
    para dar forma ao registro final que será gravado no arquivo .json

    Args:
        file_in: Endereço do arquivo no formato OSM/XML que será lido
        pretty: Booleano que indica se o parametro de gravação com recuo 2
    Returns:
        Não retorna objeto
    """
    # Nomeia o arquivo de saída
    file_out = "{0}.json".format(file_in)
    data = []
    # Abre o arquivo json no modo de escrita
    with codecs.open(file_out, "w") as fo:
        # Percorre cada elemento do arquivo             
        for _, element in ET.iterparse(file_in):
            # Chama o método para configurar cada campo
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    # Grava o elemento formatado no arquivo .json
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    

if __name__ == "__main__":
    process_map("C:/Nanodegree/MongoDb/Trab_final/sample_BH.osm", True)