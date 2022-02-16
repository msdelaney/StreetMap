import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict

import os
#Set the proper current working directory
os.getcwd()
os.chdir('C:\Python27\Scripts\proj2-MDB')


def count_tags(filename):
        tcount = {}
        for event,elem in ET.iterparse(filename):
            tag = elem.tag
            if tag in tcount: 
                tcount[tag] += 1
            else:
                tcount[tag] = 1
        return tcount
            
           
            


tags = count_tags('chattanooga_tennessee.osm')
pprint.pprint(tags)