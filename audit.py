import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import string

OSMFILE = "chattanooga_tennessee.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons", "Circle", "Highway", 'Terrace', "Way", 'Run', 'Pike']

# i want to go back and change the strings to have everything checked against a lower case,
# but will probably implement later since im hitting a deadline
mapping = { "St": "Street",
            'pike':'Pike',
            "St.": "Street",
            'Ave': 'Avenue',
            'Rd.': 'Road',
            'RDG': 'Ridge',
            'Dr': 'Drive',
            'Ln': 'Lane',
            'Rd': 'Road',
            'dr.': 'Drive',
            'lane':'Lane',
            'ave.':'Avenue',
            'drive':'Drive',
            'Hwy': 'Highway',
            'court': 'Court',
            'Blvd.': 'Boulevard',
            'st': 'Street',
            'Blvd': 'Boulevard',
            'Cir':'Circle',
            'street': "Street",
            "way": "Way",
            'Dr.': 'Drive',
            'blvd':'Boulevard',
            'ave': 'Avenue',
            'rd':'Road',
            'circle': 'Circle',
            'ct': 'Court',
            'cir': 'Circle',
            'terr': 'Terrace',
            'road': 'Road',
            'Ct': 'Court',
            }
direction = {'North':'North',
             'East':'East',
             'South':'South',
             'West':'West',
             'W':'West',
             'E': 'East',
             'N': 'North',
             'S': 'South'
             }
hwy = ['153','58']
skip = ['Strikers', 'rivermont']
addst = {'Cone': 'Lane', 'vine': 'Street','creek': 'Road','McCahill': 'Road'}
check = {'Siganl':'Signal','courtnry':'Courtney','oakhill':'Oak Hill'}
            
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_poscode(elem):
    return (elem.attrib['k'] == 'addr:postcode')

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    poscode = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                #if is_street_name(tag):
                #    audit_street_type(street_types, tag.attrib['v'])
                if is_poscode(tag):
                    tag.attrib['v'] = update_poscode(tag.attrib['v'])
                    audit_poscode(poscode,tag.attrib['v'])
    elem.clear() #clear from memory
    return street_types, poscode

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def removeNum(name):
    combine =[]
    stnum = None
    #remove numbers here
    if RepresentsInt(name.split()[0]):
        stnum = name.split()[0]
        for x in name.split()[1:]:
            combine.append(x)
        name = ' '.join(combine)
        return name,stnum
    else:
        return name,stnum

def spellcheck(name):
    combine =[]
    if string.capwords(name.split()[0]) == "Brown" and string.capwords(name.split()[1]) == 'Town':
        name = 'Browntown Road'
    for x in name.split():
        if x in check.keys():
            x = check[x]
        combine.append(x)
    name = ' '.join(combine)
    return name
        
def directionFix(name): #if there is a direction in the address it moves it to the front of the street and makes it the full word
    combine =[]
    if name.split()[-1] in direction.keys():     
        combine.append(direction[name.split()[-1]])
        for x in name.split():
            if x == name.split()[-1]:
                x = ''
            combine.append(x)
        name = ' '.join(combine)
    elif name.split()[0] in direction.keys():
        for x in name.split():
            if x in direction.keys():
                x = direction[x]
            combine.append(x)
        name = ' '.join(combine)
    return name
    
        
def update_name(name, mapping = mapping):
    combine =[]
    #remove numbers here
    
    name, stnum = removeNum(name)
    name = spellcheck(name)
    name = directionFix(name)
    
    #Highways
    if name.split()[-1] in hwy:
        name = "Highway " + str(name.split()[-1])
        name = string.capwords(name)
    if name.split()[-1] == 'TN':
        name = 'Highway 58'
    #school
    if name.split()[-1] == 'School':
        return 'Central High School', stnum
    #additive fixes
    if name.split()[-1] in addst.keys():
        for x in name.split():
            combine.append(x)
        combine.append(addst[name.split()[-1]])
        name = ' '.join(combine)
        #return string.capwords(name), stnum
    #one off changes
    if name.split()[-1] == '102':
       stnum = 102
       name = 'Market Street'
    #Normal mapping
    for x in name.split():
        if x in mapping.keys():
            x = mapping[x]
        combine.append(x)
    name = ' '.join(combine)
    return string.capwords(name),stnum

def audit_poscode(poscode,code):
    if code in poscode.keys():
        poscode[code] = poscode[code] + 1
    else:
        poscode[code] = 1
    return poscode


    
def update_poscode(code):
    man = code.split()
    if code == '00003-7419':
        return '37419'
    if len(man) > 1:
        return man[-1]
    if len(man[0]) != 5:
        return None
    if not RepresentsInt(code):
        return None
    return code
 
    
st_types,poscodef = audit(OSMFILE)
pprint.pprint(dict(st_types))
pprint.pprint(dict(poscodef))
'''
for x, y in st_types.iteritems():
    if x not in mapping.keys() and x not in direction and x not in hwy and x != 'School' and x != 'TN' and x not in addst:
        print x,'  ',y

print '\n'
        
for st_type, ways in st_types.iteritems():
    for name in ways:
        better_name = update_name(name, mapping)
        print name, "=>", better_name
'''