#!/usr/bin/env python
from buildshell import *


def player_block(songs):
    block="""<section>
    <audio id="main_player">Sorry, you need HTML 5</audio>
    <div class="player">
    	<div class="playerbuttons">
            <div class="rTable">
                <div class="rTableRow">
                    <div class="rTableCell playerbutton"><button id="bPrevSong" onclick="prevSong()"><img id="bPrevSong_img" src="SITEROOT/images/prev.png" alt="Previous"></button></div>
    		        <div class="rTableCell playerbutton"><button id="bPlayPause" onclick="togglePlayPause()"><img id="bPlayPause_img" src="SITEROOT/images/play.png" alt="Play"></button></div>
    		        <div class="rTableCell playerbutton"><button id="bNextSong" onclick="nextSong()"><img id="bNextSong_img" src="SITEROOT/images/next.png" alt="Next"></button></div>
                </div>
            </div>
    	</div>
    </div>
    </section>"""   
    block+="""<section>
                <div class="songlist">
                    <ol id="playlist">"""
    for song in songs:
        block+=indexed_song_list_item_block(song,songs.index(song))  
    block+="""</ol>
            </div>
        </section>"""
    return block
    
def now_playing_block(songs):
    block="""<section>
    <div id="now_playing"><div class="tab_title">Now playing</div>"""
    for song in songs:
        block+=indexed_song_block(song,songs.index(song))
    block+='</div>'
    return block
    
        
        
def album_table_block(albums,columns):
    done=False
    counter=0
    block='<div class="album_table rTable">'
    while not done:
        block+='<div class="rTableRow">'
        for i in range(counter, counter+columns):
            if i<len(albums): 
                block+=album_table_item_block(albums[i])
            else:
                done=True
        block+='</div>'
        counter += columns
    block +='</div>'
    return block
       
    
def playlist_table_block(playlists,columns):
    done=False
    counter=0
    block='<div class="playlist_table rTable">'
    while not done:
        block+='<div class="rTableRow">'
        for i in range(counter, counter+columns):
            if i<len(playlists): 
                block+=playlist_table_item_block(playlists[i])
            else:
                done=True
        block+='</div>'
        counter += columns
    block +='</div>'
    return block
     
#make index page - this shows the most recent album with the option to see more
for p in playlists:
    if p.name == showcase_name:
        showcase_playlist=p


with open(build_dir+'index.html','w') as templ:
    content="""<div id="player_container">
                    <div id="player_source_container">"""
    try:
        content+=playlist_block(showcase_playlist)
        content+=player_block(showcase_playlist.tracks())
        content+="""</div>
                    <div id="now_playing_container">"""
        content+=now_playing_block(showcase_playlist.tracks())
    except:
        album=album_list(True)[0]
        content+=album_block(album)     
        content+=player_block(album.tracks());
        content+="""</div>
                    <div id="now_playing_container">"""
        content+=now_playing_block(album.tracks())
    content+='</div></div>'
    templ.write(fill_in_page(bandname,content).encode('utf8')) 

#Build Explore by Album
with open(build_dir+'albums.html','w') as templ:
    content='<div class="explore_album">'
    content+='<header class="content_header">Explore by Album</header>'
    content+=album_table_block(album_list(True),5)
    content+='</div>'
    templ.write(fill_in_page('Albums by '+bandname,content).encode('utf8'))
    
#Build Explore by Playlist
with open(build_dir+'playlists.html','w') as templ:
    content='<div class="explore_playlist">'
    content+='<header class="content_header">Explore All Playlists</header>'
    content+='<h1>Misc Playlists</h1>'
    content+=playlist_table_block(misc_playlists,5)
    content+='<h1>Tag Playlists</h1>'
    content+=playlist_table_block(tag_playlists,5)
    content+='<h1>Genre Playlists</h1>'
    content+=playlist_table_block(genre_playlists,5)
    content+='</div>'
    templ.write(fill_in_page('Playlists by '+bandname,content).encode('utf8'))
    
#Build Explore by Tags
with open(build_dir+'tags.html','w') as templ:
    content='<div class="explore_tags">'
    content+='<header class="content_header">Explore by Tags</header>'
    content+=playlist_table_block(tag_playlists,5)
    content+='</div>'
    templ.write(fill_in_page('Tag Playlists by '+bandname,content).encode('utf8'))
    
#Build Explore by Genre
with open(build_dir+'genres.html','w') as templ:
    content='<div class="explore_genre">'
    content+='<header class="content_header">Explore by Genre</header>'
    content+=playlist_table_block(genre_playlists,5)
    content+='</div>'
    templ.write(fill_in_page('Genre Playlists by '+bandname,content).encode('utf8'))

# build each album page
for album in album_list():
    page_title=album.albumname+' by '+ album.albumartist
    with open(build_albums+album.safe_name+".html",'w') as templ:
        content="""<div id="player_container">
                    <div id="player_source_container">"""
        content+=album_block(album)
        content+=player_block(album.tracks());
        content+="""</div>
                    <div id="now_playing_container">"""
        content+=now_playing_block(album.tracks())
        content+='</div></div>'
        templ.write(fill_in_page(page_title,content).encode('utf8'))
        
# build each playlist page
for playlist in playlists:
    page_title=playlist.name+' by '+ bandname
    with open(build_playlists+playlist.safe_name+".html",'w') as templ:
        content="""<div id="player_container">
                    <div id="player_source_container">"""
        content+=playlist_block(playlist)
        content+=player_block(playlist.tracks());
        content+="""</div>
                    <div id="now_playing_container">"""
        content+=now_playing_block(playlist.tracks())
        content+='</div></div>'
        templ.write(fill_in_page(page_title,content).encode('utf8'))
        
        
        
      