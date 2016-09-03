#!/usr/bin/env python
import os
import shutil

directories=["css","images","scripts","templates"]
files=["buildsite.py","siteinfo.py","robots.txt"]


#Set the skin
skin="playlist-based"



skindir="skins/"+skin+"/"
base="./"


# copy the files and directories to current
for dir in directories:
    shutil.copytree(skindir+dir,base+dir)

for file in files:
    shutil.copy(skindir+file,base)


# build the site
import buildsite

# remove copied files and directories
import cleanup

