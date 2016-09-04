#!/usr/bin/env python
from helpers import safe

class Playlist:
    'an curated list of songs from different albums'
    
    def __init__(self,name):
        self.name=name
        self.safe_name=safe(self.name)
        self.download_link="PROD_MEDIA"+self.safe_name+".zip" 
        self.page="PROD_PLAYLISTS"+self.safe_name+".html"    
        self.__tracks=[]
        self.count=str(0)
        
    def addSong(self,song):
        self.__tracks.append(song)
        self.count=str(len(self.__tracks))
        
    def addSongList(self,songs):
        self.__tracks+=songs
        self.count=str(len(self.__tracks))
        
    def tracks(self):
        return self.__tracks
     
        