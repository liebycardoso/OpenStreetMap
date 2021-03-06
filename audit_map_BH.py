#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Thu Dec 22 16:32:07 2016

@author: MasterLieby
"""

import re

def audit_street_type(street_types, street_name, expected_street):
    """
    Audita o registro informado e verifica com auxilio do Regex o tipo da rua

    """
    street_type_re = re.compile(r'^\b(?u)\w\S+\.?', re.IGNORECASE)
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected_street:
            street_types[street_type].add(street_name)
            
    return street_types

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
    return (elem.attrib['k'] == "addr:postal_code")    

def update_postal_code(postalcode):   
    """
    Para cada valor de postalcode recebido compara com o padrão passada e retorna a primeira 
    posição da lista de valores.
    Na sequencia exclui o caractere "-" da string.
    
    Args:
        postalcode: String com a representação do código postal
    Returns:
        postalcode: Versão da string recebida sem o caractere "-"
    """           
    
    postal_code_re = re.findall(r'^(\d{5})-(\d{3})$', postalcode)[0]
    postalcode = postal_code_re.replace("-","")
        
    return postalcode


def update_street_type(name, mapping, expected_street):
    """
    Recebe o nome de uma rua e:
    1) Identifica a primera string que é o tipo da rua
    2) Verifica se esse tipo é um dos tipos esperados (expected_street)
    3) Se não for, tenta substituir a string por uma mapeada no dict mapping
    4) Se a string não existir como chave no mapping, inclui a string Rua como tipo pre-definido

    Args:
        name: Nome da rua
        mapping: Dicionário com o DE/PARA dos tipos de rua
        expected_street: Lista de tipos de ruas aceitos
    Returns:
        Retorna o nome da rua formatado
    """
    street_type_re = re.compile(r'^\b(?u)\w\S+\.?', re.IGNORECASE)

    name = name.title()
    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        
        if street_type not in expected_street:
            try:
                name = re.sub(street_type_re, mapping[street_type], name)
            except:
                
                name = "Rua " + name  
                
    return name

def update_street_title(name, mapping):   
    """
    Recebe o nome de uma rua e:
    1) Identifica a segunda string do nome como possivel valor de title
    2) Verifica se esse valor de title termina com ".", o que na base de bh é a versão abreviada
    3) Em caso positivo, substituí a string por uma mapeada no dict mapping

    Args:
        name: Nome da rua
        mapping: Dicionário com o DE/PARA dos titulos das pessoas (Professor, Capitão)
    Returns:
        Retorna o nome da rua formatado
    """
    title = name.split()[1]
    
    if title.endswith("."):
        if mapping[title]:
            name = name.replace(title,mapping[title])              
        
    return name

def update_city(city, mapping, expected_city):   
    """
    Recebe o nome da cidade:
    1) Capitaliza a primera letra de cada String e atribui o valor à variável city
    2) Verifica se o nome da cidade está no dicionário de nomes esperados
    3) Em caso positivo, substituí a string por uma mapeada no dict mapping
    4) Se a substituição falhar e a string começar com Belo, city recebe uma versão de 14
        caracteres da string. Essa opção corrige algumas strings que tem no nome da cidade + estado

    Args:
        city: Nome da cidade
        mapping: Dicionário com o DE/PARA do nome das cidades
        expected_city: Lista de nomes de cidades aceitas
    Returns:
        Retorna o nome da cidade formatado
    """
            
    city = city.title()   
       
    if city not in expected_city:
        try:
            city = city.replace(city, mapping[city])
        except:
            
            if city.startswith("Belo"):
                city = city[0:14]
        
    return city

def main():
    pass

if __name__ == "__main__":
    main()