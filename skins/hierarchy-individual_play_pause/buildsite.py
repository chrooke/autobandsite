#!/usr/bin/env python
from buildshell import *

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
    page_title=album.albumname+' by '+ bandname
    with open(build_albums+album.safe_name+".html",'w') as templ:
        content=album_block(album)
        content+='\n<section>\n<div class=songlist">\n<ol>\n'
        for song in album.tracks():
            content+=song_list_item_block(song)  
        content+='\n</ol>\n</div>\n</section>\n'  
        templ.write(fill_in_page(page_title,content).encode('utf8'))
        
#for song in songs:
    page_title=song.title+' by '+ song.artist
    with open(build_songs+song.safe_name+".html",'w') as templ:
        content=song_block(song)
        templ.write(fill_in_page(page_title,content).encode('utf8'))