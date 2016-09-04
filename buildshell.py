#!/usr/bin/env python
import os
import shutil
from mutagen import File
from helpers import *
from Song import *
from Album import *
from Playlist import *
from siteinfo import *

##GLOBALS

#directories
css="css"
templates="templates/"
images="images/"
scripts="scripts/"

songfiles="songfiles/"

build_dir="../autobandsite-build/"
build_css=build_dir+"css/"
build_media=build_dir+"media/"
build_images=build_dir+"images/"
build_scripts=build_dir+"scripts/"
build_songs=build_dir+"songs/"
build_albums=build_dir+"albums/"
build_playlists=build_dir+"playlists/"

prod_css=siteurl+"css/"
prod_media=siteurl+"media/"
prod_images=siteurl+"images/"
prod_scripts=siteurl+"scripts/"
prod_songs=siteurl+"songs/"
prod_albums=siteurl+"albums/"
prod_playlists=siteurl+"playlists/"

#data structures
songs=[]
albumdict={}
albums=[]
playlists=[]
tags=set([])
genres=set([])
tag_playlists=[]
genre_playlists=[]

#template filenames
base_templ=templates+'base.tmpl'
song_list_item_block_templ=templates+'song_list_item_block.tmpl'
song_block_templ=templates+'song_block.tmpl'
album_table_item_block_templ=templates+'album_table_item_block.tmpl'
album_block_templ=templates+'album_block.tmpl'
playlist_table_item_block_templ=templates+'playlist_table_item_block.tmpl'
playlist_block_templ=templates+'playlist_block.tmpl'
abs_js_templ=templates+'abs.js.tmpl'


#flatten(album_attrs)
site_tags = {   'SITEURL':siteurl,
                'SITEOWNER':siteowner,
                'SITEYEAR':siteyear,
                'PROD_IMAGES':prod_images,
                'PROD_ALBUMS':prod_albums,
                'PROD_SONGS':prod_songs,
                'PROD_MEDIA':prod_media,
                'PROD_PLAYLISTS':prod_playlists,
            }
         
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
    return block

def song_list_item_block(song):
    with open(song_list_item_block_templ,'r') as templ:
        block=templ.read()
        for attr in pub_attrs(song):
            block=re.compile(attr.upper()).sub(getattr(song,attr),block)      
        return block
        
def indexed_song_list_item_block(song,index):
    block=song_list_item_block(song)
    block=re.compile('INDEX').sub(str(index),block)
    return block
        
def song_block(song):
    with open(song_block_templ,'r') as templ:
        block=templ.read()
        for attr in pub_attrs(song):
            block=re.compile(attr.upper()).sub(getattr(song,attr),block)         
        return block
        
def indexed_song_block(song,index):
    block=song_block(song)
    block=re.compile('INDEX').sub(str(index),block)
    return block

def album_table_item_block(album):
    with open(album_table_item_block_templ,'r') as templ:
        block=templ.read()
        for attr in pub_attrs(album):
            block=re.compile(attr.upper()).sub(getattr(album,attr),block)       
        return block
    
def album_block(album):
    with open(album_block_templ,'r') as templ:
        block=templ.read()
        for attr in pub_attrs(album):
            block=re.compile(attr.upper()).sub(getattr(album,attr),block)       
        return block
        
def playlist_block(playlist):
    with open(playlist_block_templ,'r') as templ:
        block=templ.read()
        for attr in pub_attrs(playlist):
            block=re.compile(attr.upper()).sub(getattr(playlist,attr),block)         
        return block
        
def playlist_table_item_block(playlist):
    with open(playlist_table_item_block_templ,'r') as templ:
        block=templ.read()
        for attr in pub_attrs(playlist):
            block=re.compile(attr.upper()).sub(getattr(playlist,attr),block)         
        return block

## MAIN CODE

#remove existing build directory and recreate
try:
    shutil.rmtree(build_dir)
except:
    pass
os.mkdir(build_dir,0755)
os.mkdir(build_media,0755)
os.mkdir(build_songs,0755)
os.mkdir(build_albums,0755)
os.mkdir(build_playlists,0755)

#copy robots.txt
shutil.copy('robots.txt',build_dir)

#copy scripts, images, and css
shutil.copytree(scripts,build_scripts)
shutil.copytree(css,build_css)
shutil.copytree(images,build_images)

#run certain scripts through the template process while copying
with open(build_scripts+'abs.js','w') as target:
    with open(abs_js_templ,'r') as templ:
        target.write(templ.read().replace('SITEURL',siteurl))

# populate the songs and albums lists, copy the song files, and generate album artwork

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
    art=album.artwork()
    if art:
        with open(build_images+album.artwork_filename,'wb') as img:
            img.write(art)
    else:
        shutil.copyfile(images+"default.jpg",build_images+album.artwork_filename)

#make set of song tags and genres
for song in songs:
    for tag in song.tags():
        tags.add(tag)
    if song.genre: genres.add(song.genre)
        
#pre-generate a playlist for each tag
for tag in tags:
    playlist=Playlist(tag)
    songlist=set([])
    for song in songs:
        if tag in song.tags():
            songlist.add(song)
    playlist.addSongList(songlist)
    tag_playlists.append(playlist)
        
#pre-generate a playlist for each tag
for genre in genres:
    playlist=Playlist(genre)
    songlist=set([])
    for song in songs:
        if genre == song.genre:
            songlist.add(song)
    playlist.addSongList(songlist)
    genre_playlists.append(playlist)
    
playlists=tag_playlists+genre_playlists
            
            

# Now we have the raw material to actually generate web pages
