#!/usr/bin/env python
import os
import shutil

directories=["css","images","scripts","templates"]
files=["buildsite.py","siteinfo.py","robots.txt"]


#Set the skin
skin="playlist-based"



skindir="skins/"+skin+"/"
base="./"

try:
    # copy the files and directories to current
    for dir in directories:
        shutil.copytree(skindir+dir,base+dir)

    for file in files:
        shutil.copy(skindir+file,base)
    # build the site
    #import buildsite
#    import buildsite
    from buildsite import *
except Exception as e:
    print(e);
    print "Uh-oh! There was an error. Site not built. Cleaning up."

# remove copied files and directories
import cleanup

