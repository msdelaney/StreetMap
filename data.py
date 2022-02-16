#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from audit import update_name, update_poscode

file_in = 'chattanooga_tennessee.osm'


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

skip = ['Strikers', 'rivermont']
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    node["created"]={}
    node["address"]={}
    node["pos"]=[]
    refs=[]
    
    if element.tag == "node" or element.tag == "way":
        if 'id' in element.attrib:
            node['id']=element.attrib['id']
        node['type'] = element.tag
        
        if 'visible' in element.attrib.keys():
            node['visible']=element.attrib['visible']
        
        for elem in CREATED:
            if elem in element.attrib:
                node['created'][elem]=element.attrib[elem]
        if 'lat' in element.attrib:
            node["pos"].append(float(element.attrib["lat"]))
        if "lon" in element.attrib:
            node["pos"].append(float(element.attrib["lon"]))
        
        for tag in element.iter('tag'):
            if not(problemchars.search(tag.attrib['k'])):
                if tag.attrib['k'] == 'addr:housenumber':
                    node['address']['housenumber'] = tag.attrib['v']
                if tag.attrib['k'] == 'addr:postcode':
                    node['address']['postcode'] = update_poscode(tag.attrib['v'])
                if tag.attrib['k'] == "addr:street":  
                    updatename, stnum = update_name(tag.attrib['v'])
                    node["address"]["street"] =  updatename
                    if stnum != None: #Some of the street names have the number as well
                        node['address']['housenumber'] = stnum
                if tag.attrib['k'].find("addr")==-1:
                    node[tag.attrib['k']]=tag.attrib['v']
       
        for nd in element.iter("nd"):
             refs.append(nd.attrib["ref"])
        if node["address"] =={}:
            node.pop("address", None)
        if refs != []:
           node["node_refs"]=refs 
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
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data
    
data = process_map(file_in, False)