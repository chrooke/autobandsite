#!/usr/bin/env python

import os
import shutil
import re
from collections import defaultdict
from mutagen import File


##GLOBALS

# band info
bandname="Chris Cooke"

#directories
css="css"
templates="templates/"
songfiles="songfiles/"
images="images/"
build_dir="../autobandsite-build/"
build_css=build_dir+"css/"
build_media=build_dir+"media/"
build_images=build_dir+"images/"

#data structures
songs={}
tracks=defaultdict(list)

#template filenames
base_templ=templates+'base.tmpl'
album_block_templ=templates+'album_block.tmpl'
song_list_item_block_templ=templates+'song_list_item_block.tmpl'
song_block_templ=templates+'song_block.tmpl'

#template substitusions
song_attrs = ['TITLE','ALBUMNAME','YEAR','TRACK', 'COPYRIGHT','BPM','ARTIST','ALBUMPAGE','SONGPAGE','GENRE','COMPOSER','COPYRIGHT','DOWNLOAD_LINK','COVER_ART']

###HELPER FUNCTIONS

## General helpers
#Makes a string safe to use as a file name
# replaces spaces with _
# removes any characters except alphanumeric,_,or .
def forfilename(item):
    #replace spaces with underscores
    item = re.compile('\s').sub('_',item)
    #remove non alphanum,_, or .
    item = re.compile('[^\w\d_\.]').sub('',item)
    return item

## Metatdata helpers
def filename(song):
    return forfilename(song)

def read_text_tag(song,tag):
    try:
        return songs[song].tags[tag].text[0].encode('ascii','ignore')
    except:
        return ''
        
def read_data_tag(song,tag):
    try:
        return songs[song].tags[tag].data
    except:
        return None

def albumname(song):
    return read_text_tag(song,'TALB')
        
def year(song):
    return read_text_tag(song,'TDRC')

def track(song):
     return read_text_tag(song,'TRCK').split('/')[0]  
     
def title(song):
    return read_text_tag(song,'TIT2')    

def copyright(song):
    return read_text_tag(song,'COMM::eng')
    
def bpm(song):
    return read_text_tag(song,'TBPM')

def artist(song):
    return read_text_tag(song,'TPE1')  
    
def genre(song):
    return read_text_tag(song,'TCON') 
    
def composer(song):
    return read_text_tag(song,'TCOM') 
     
def artwork(song):
     return read_data_tag(song,'APIC:')
     
def cover_art(song):
    return album_art_file(albumname(song))
     
def albumpage(song):
    return forfilename(albumname(song))+'.html'
    
def songpage(song):
    return forfilename(song)[:-4]+'.html' #slice on song name removes .mp3
    
def download_link(song):
    return build_media+forfilename(song)
     
# more helpers

def song_from_album(album):
    return tracks[album][0][1]
    
def album_data(album,data):
        return data(song_from_album(album))   
 
def album_art_file(album):
    return build_images+forfilename(album_data(album,albumname))+".jpg"
        
def album_list(reverse=False):
    album_list=tracks.keys()
    album_list.sort(key=lambda x:album_data(x,year),reverse=reverse)
    return album_list

# templating helpers
def fill_in_page(title,contents):
    with open(base_templ,'r') as templ:
        block=templ.read().replace('TITLE_BLOCK',title)
        block=block.replace('CONTENT_BLOCK',contents)
    return block

def song_list_item_block(song):
    with open(song_list_item_block_templ,'r') as templ:
        block=templ.read()
        for attr in song_attrs:
            block=re.compile(attr).sub(globals()[attr.lower()](song),block)         
        return block
        
def song_block(song):
    with open(song_block_templ,'r') as templ:
        block=templ.read()
        for attr in song_attrs:
            block=re.compile(attr).sub(globals()[attr.lower()](song),block)         
        return block

def album_block(album):
    with open(album_block_templ,'r') as templ:
        block=templ.read()
        for attr in song_attrs:
            block=re.compile(attr).sub(album_data(album,globals()[attr.lower()]),block)         
        return block

## MAIN CODE

#remove existing build directory and recreate
try:
    shutil.rmtree(build_dir)
except:
    pass
os.mkdir(build_dir,0755)
os.mkdir(build_css,0755)
os.mkdir(build_media,0755)
os.mkdir(build_images,0755)

#copy robots.txt
shutil.copy('robots.txt',build_dir)

#pull metadata from mp3s, building the songs data structure, and copy them to the media directory
for song in os.listdir(songfiles):
    if song.endswith('.mp3'):
        #get metadata from mp3 files
        songs[song]=File(songfiles+song)
        #copy song file to site, sanitizing filename
        shutil.copyfile(songfiles+song,build_media+forfilename(song))


#build the tracks data structure
for song in songs.keys():
    if albumname(song):
        tracks[albumname(song)].append((int(track(song)),song))
    else:
        pass #songs without album names get skipped


#sort each album's tracks by track number, generate album art
for album in tracks.keys():
    tracks[album].sort(key=lambda x:x[0])
    art=album_data(album,artwork)
    if art:
        with open(album_art_file(album),'wb') as img:
            img.write(art)
    else:
        shutil.copyfile(images+"default.jpg",album_art_file(album))


#make index page - this shows the most recent album with the option to see more
with open(build_dir+'index.html','w') as templ:
    content=album_block(album_list(True)[0])
    content+='<a href=albums.html>See more albums.</a>'
    templ.write(fill_in_page(bandname,content))

#Build music page - this lists all albums
with open(build_dir+'albums.html','w') as templ:
    content=''
    for album in album_list(True):
        content+=album_block(album)
    templ.write(fill_in_page('Albums by '+bandname,content))

# build each album page
for album in album_list():
    page_title=album_data(album,albumname)+' by '+bandname
    with open(build_dir+album_data(album,albumpage),'w') as templ:
        content=album_block(album)
        for tracknum,song in tracks[album]:
            content+=song_list_item_block(song)     
        templ.write(fill_in_page(page_title,content))
        
#Build each song page
for song in songs.keys():
    page_title=title(song)+' by '+artist(song)
    with open(build_dir+songpage(song),'w') as templ:
        content=song_block(song)
        templ.write(fill_in_page(page_title,content))
    