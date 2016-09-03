#!/usr/bin/env python
import re

## General helpers
    
#Makes a string safe to use as a file name
# replaces spaces with _
# removes any characters except alphanumeric,_,or .
def safe(item):
    #replace spaces with underscores
    item = re.compile('\s').sub('_',item)
    #remove non alphanum,_, or .
    item = re.compile('[^\w\d_\.]').sub('',item)
    return item.encode('ascii','ignore')
    
