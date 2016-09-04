#!/usr/bin/env python
from buildshell import *


def player_block(songs):
    block="""<section>
    <audio id="main_player">Sorry, you need HTML 5</audio>
    <div class="player">
    	<div class="playerbuttons">
            <div class="rTable">
                <div class="rTableRow">
                    <div class="rTableCell"><button id="bPrevSong" onclick="prevSong()"><img id="bPrevSong_img" src="SITEURLimages/prev.png" alt="Previous"></button></div>
    		        <div class="rTableCell"><button id="bPlayPause" onclick="togglePlayPause()"><img id="bPlayPause_img" src="SITEURLimages/play.png" alt="Play"></button></div>
    		        <div class="rTableCell"><button id="bNextSong" onclick="nextSong()"><img id="bNextSong_img" src="SITEURLimages/next.png" alt="Next"></button></div>
                </div>
            </div>
    	</div>
    </div>
    </section>"""   
#   content+='<audio id="main_player" preload="auto" tabindex="0" controls="" type="audio/mpeg"><source type="audio/mp3" src="">Sorry, your browser does not support HTML5 audio.</audio>'
    block+='\n<section>\n<div class="songlist">\n<ol id="playlist">\n'
    for song in songs:
        block+=indexed_song_list_item_block(song,songs.index(song))  
    block+='\n</ol>\n</div>\n</section>\n' 
    block+='<div id="now_playing">Now playing' 
    for song in songs:
        block+=indexed_song_block(song,songs.index(song))
    block+='</div>'
    return block
    
        
        
def album_table_block(albums,columns):
    done=False
    counter=0
    block='<div class="rTable">'
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
    block='<div class="rTable">'
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
    if p.name == "showcase":
        showcase_playlist=p


with open(build_dir+'index.html','w') as templ:
    try:
        content=playlist_block(showcase_playlist)
        content+=player_block(showcase_playlist.tracks());
    except:
        album=album_list(True)[0]
        content=album_block(album)     
        content+=player_block(album.tracks());
    templ.write(fill_in_page(bandname,content).encode('utf8')) 

#Build Explore by Album
with open(build_dir+'albums.html','w') as templ:
    content='<header class="content_header">Explore by Album</header>'
    content+=album_table_block(album_list(True),4)
    templ.write(fill_in_page('Albums by '+bandname,content).encode('utf8'))
    
#Build Explore by Playlist
with open(build_dir+'playlists.html','w') as templ:
    content='<header class="content_header">Explore All Playlists</header>'
    content+=playlist_table_block(tag_playlists,4)
    content+='<h1>Genre Playlists</h1>'
    content+=playlist_table_block(genre_playlists,4)
    templ.write(fill_in_page('Playlists by '+bandname,content).encode('utf8'))
    
#Build Explore by Tags
with open(build_dir+'tags.html','w') as templ:
    content='<header class="content_header">Explore by Tags</header>'
    content+=playlist_table_block(tag_playlists,4)
    templ.write(fill_in_page('Tag Playlists by '+bandname,content).encode('utf8'))
    
#Build Explore by Genre
with open(build_dir+'genres.html','w') as templ:
    content='<header class="content_header">Explore by Genre</header>'
    content+=playlist_table_block(genre_playlists,4)
    templ.write(fill_in_page('Genre Playlists by '+bandname,content).encode('utf8'))

# build each album page
for album in album_list():
    page_title=album.albumname+' by '+ bandname
    with open(build_albums+album.safe_name+".html",'w') as templ:
        content=album_block(album)
        content+=player_block(album.tracks());
        templ.write(fill_in_page(page_title,content).encode('utf8'))
        
# build each playlist page
for playlist in playlists:
    page_title=playlist.name+' by '+ bandname
    with open(build_playlists+playlist.safe_name+".html",'w') as templ:
        content=playlist_block(playlist)
        content+=player_block(playlist.tracks());
        templ.write(fill_in_page(page_title,content).encode('utf8'))
        
        
        
      