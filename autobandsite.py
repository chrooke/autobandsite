#!/usr/bin/env python
import os
import shutil

css="css"
images="images"
scripts="scripts"
templates="templates"

base="./"
basecss=base+css
baseimages=base+images
basescripts=base+scripts
basetemplates=base+templates

#Get the skin
skin="hierarchy-individual_play_pause"
skindir="skins/"+skin+"/"
skincss=skindir+css
skinimages=skindir+images
skinscripts=skindir+scripts
skintemplates=skindir+templates



# copy the files and directories to current
shutil.copytree(skincss,basecss)
shutil.copytree(skinimages,baseimages)
shutil.copytree(skinscripts,basescripts)
shutil.copytree(skintemplates,basetemplates)
shutil.copy(skindir+'buildsite.py',base)
shutil.copy(skindir+'siteinfo.py',base)
shutil.copy(skindir+'robots.txt',base)

# build
import buildsite

# remove copied files and directories
shutil.rmtree(basecss)
shutil.rmtree(baseimages)
shutil.rmtree(basescripts)
shutil.rmtree(basetemplates)
os.remove(base+'buildsite.py')
os.remove(base+'siteinfo.py')
os.remove(base+'robots.txt')

