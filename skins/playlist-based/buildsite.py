#!/usr/bin/env python
from buildshell import *




def player_block(songs):
    block="""<section>
    <audio id="main_player">Sorry, you need HTML 5</audio>
    <div class="player">
    	<div class="playerbuttons">
            <button id="bPrevSong" onclick="prevSong()"><img id="bPrevSong_img" src="SITEURLimages/prev.png" alt="Previous"></button>
    		<button id="bPlayPause" onclick="togglePlayPause()"><img id="bPlayPause_img" src="SITEURLimages/play.png" alt="Play"></button>
    		<button id="bNextSong" onclick="nextSong()"><img id="bNextSong_img" src="SITEURLimages/next.png" alt="Next"></button>
    	</div>
    </div>
    </section>"""   
#   content+='<audio id="main_player" preload="auto" tabindex="0" controls="" type="audio/mpeg"><source type="audio/mp3" src="">Sorry, your browser does not support HTML5 audio.</audio>'
    block+='\n<section>\n<div class="songlist">\n<ol id="playlist">\n'
    for song in songs:
        block+=indexed_song_list_item_block(song,songs.index(song))  
    block+='\n</ol>\n</div>\n</section>\n'  
    for song in songs:
        block+=indexed_song_block(song,songs.index(song))
    return block
    
#make index page - this shows the most recent album with the option to see more
for p in playlists:
    if p.name == "showcase":
        showcase_playlist=p


with open(build_dir+'index.html','w') as templ:
    try:
        content=playlist_block(showcase_playlist)
        content+=player_block(showcase_playlist.tracks());
        content+='<a href=playlists.html>See more playlists.</a>'
    except:
        album=album_list(True)[0]
        content=album_block(album)     
        content+=player_block(album.tracks());
        content+='<a href=albums.html>See more albums.</a>'
    templ.write(fill_in_page(bandname,content).encode('utf8')) 

#Build music page - this lists all albums
with open(build_dir+'albums.html','w') as templ:
    content=''
    for album in album_list(True):
        content+=album_block(album)
    templ.write(fill_in_page('Albums by '+bandname,content).encode('utf8'))
    
#Build music page - this lists all playlists
with open(build_dir+'playlists.html','w') as templ:
    content='<h1>Curated Playlists</h1>'
    for playlist in tag_playlists:
        content+=playlist_block(playlist)
    content+='<h1>Genre Playlists</h1>'
    for playlist in genre_playlists:
        content+=playlist_block(playlist)
    templ.write(fill_in_page('Playlists by '+bandname,content).encode('utf8'))

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
        
        
        
      