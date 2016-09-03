#!/usr/bin/env python
import os
import shutil

directories=["css","images","scripts","templates"]
files=["buildsite.py","siteinfo.py","robots.txt"]

base="./"
base_directories=[base+x for x in directories]
base_files=[base+x for x in files]

# remove copied files and directories
for dir in base_directories:
    try:
        shutil.rmtree(dir)
    except:
        pass
        
for file in base_files:
    try:    
        os.remove(file)
    except:
        pass


# remove compiled python files
for file in os.listdir(base):
    if file.endswith('.pyc'):
        try:
            os.remove(file)
        except:
            pass