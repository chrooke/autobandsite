#!/usr/bin/env python

import os
import shutil
from mutagen import File
from helpers import *
from Song import *
from Album import *


##GLOBALS

# band info - replace this with your own info
bandname="Chris Cooke"
siteurl="http://localhost/~chris/"
siteowner="Chris Cooke"

#directories
css="css"
templates="templates/"
songfiles="songfiles/"
images="images/"
scripts="scripts/"
build_dir="../autobandsite-build/"
build_css=build_dir+"css/"
build_media=build_dir+"media/"
build_images=build_dir+"images/"
build_scripts=build_dir+"scripts/"
build_songs=build_dir+"songs/"
build_albums=build_dir+"albums/"

prod_css=siteurl+"css/"
prod_media=siteurl+"media/"
prod_images=siteurl+"images/"
prod_scripts=siteurl+"scripts/"
prod_songs=siteurl+"songs/"
prod_albums=siteurl+"albums/"

#data structures
songs=[]
albumdict={}
albums=[]

#template filenames
base_templ=templates+'base.tmpl'
album_block_templ=templates+'album_block.tmpl'
song_list_item_block_templ=templates+'song_list_item_block.tmpl'
song_block_templ=templates+'song_block.tmpl'
abs_js_templ=templates+'abs.js.tmpl'

#template substitusions
common_attrs = ['ALBUMNAME','YEAR', 'COPYRIGHT','BPM','ARTIST','GENRE','COMPOSER','COPYRIGHT','DOWNLOAD_LINK','COVER_ART','SAFE_NAME']
song_attrs = common_attrs+['TITLE','TRACK','SONGPAGE']
#flatten(song_attrs)
album_attrs = common_attrs+['ALBUMPAGE']
#flatten(album_attrs)
site_tags = {'SITEURL':siteurl,'SITEOWNER':siteowner}

         
# more helpers

        
def album_list(reverse=False):
    return sorted(albums,key=lambda x:int(x.year),reverse=reverse)

# templating helpers
def fill_in_page(title,contents):
    with open(base_templ,'r') as templ:
        block=templ.read().replace('TITLE_BLOCK',title)
        block=block.replace('CONTENT_BLOCK',contents)
        #Site tags (not related to songs. Fill in after content.
        for tag in site_tags:
            block=block.replace(tag,site_tags[tag]) 
#        block=block.replace('SITEOWNER',siteowner)
#        block=block.replace('SITEURL',siteurl)
        block=block.replace('PROD_IMAGES',prod_images)
        block=block.replace('PROD_ALBUMS',prod_albums)
        block=block.replace('PROD_SONGS',prod_songs)
        block=block.replace('PROD_MEDIA',prod_media)
    return block

def song_list_item_block(song):
    with open(song_list_item_block_templ,'r') as templ:
        block=templ.read()
        for attr in song_attrs:
            block=re.compile(attr).sub(getattr(song,attr.lower()),block)         
        return block
        
def song_block(song):
    with open(song_block_templ,'r') as templ:
        block=templ.read()
        for attr in song_attrs:
            block=re.compile(attr).sub(getattr(song,attr.lower()),block)         
        return block

def album_block(album):
    with open(album_block_templ,'r') as templ:
        block=templ.read()
        for attr in album_attrs:
            block=re.compile(attr).sub(getattr(album,attr.lower()),block)         
        return block

## MAIN CODE

#remove existing build directory and recreate
try:
    shutil.rmtree(build_dir)
except:
    pass
os.mkdir(build_dir,0755)
#os.mkdir(build_css,0755)
os.mkdir(build_media,0755)
#os.mkdir(build_images,0755)
#os.mkdir(build_scripts,0755)
os.mkdir(build_songs,0755)
os.mkdir(build_albums,0755)

#copy robots.txt
shutil.copy('robots.txt',build_dir)

#copy scripts, images, and css
shutil.copytree(scripts,build_scripts)
shutil.copytree(css,build_css)
shutil.copytree(images,build_images)

#create scripts that need to run through the template process
with open(build_scripts+'abs.js','w') as target:
    with open(abs_js_templ,'r') as templ:
        target.write(templ.read().replace('SITEURL',siteurl))


#pull metadata from mp3s, building the songs data structure, and copy them to the media directory
for song in os.listdir(songfiles):
    if song.endswith('.mp3'):
        #get metadata from mp3 files
        s=Song(song,File(songfiles+song))
        songs.append(s)
        #copy song file to site, sanitizing filename
        shutil.copyfile(songfiles+song,build_media+s.filename)

#populate the list of albums by reading the songs
for song in songs:
    if song.albumname:
        if not song.albumname in albumdict:
            albumdict[song.albumname]=Album(song)
            albums.append(albumdict[song.albumname])
        else:
            albumdict[song.albumname].addSong(song)
    else:
        pass #songs without album names get skipped
        
#generate album art files
for album in albums:
    art=album.artwork
    if art:
        with open(build_images+album.artwork_filename,'wb') as img:
            img.write(art)
    else:
        shutil.copyfile(images+"default.jpg",build_images+album.artwork_filename)


#make index page - this shows the most recent album with the option to see more
with open(build_dir+'index.html','w') as templ:
    content=album_block(album_list(True)[0])
    content+='<a href=albums.html>See more albums.</a>'
    templ.write(fill_in_page(bandname,content).encode('utf8'))

#Build music page - this lists all albums
with open(build_dir+'albums.html','w') as templ:
    content=''
    for album in album_list(True):
        content+=album_block(album)
    templ.write(fill_in_page('Albums by '+bandname,content).encode('utf8'))

# build each album page
for album in album_list():
    page_title=album.name+' by '+ bandname
    with open(build_albums+album.safe_name+".html",'w') as templ:
        content=album_block(album)
        content+='\n<section>\n<div class=songlist">\n<ol>\n'
        for song in album.tracks:
            content+=song_list_item_block(song)  
        content+='\n</ol>\n</div>\n</section>\n'  
        templ.write(fill_in_page(page_title,content).encode('utf8'))
        
#Build each song page
for song in songs:
    page_title=song.title+' by '+ song.artist
    with open(build_songs+song.safe_name+".html",'w') as templ:
        content=song_block(song)
        templ.write(fill_in_page(page_title,content).encode('utf8'))
    