#!/usr/bin/env python
from helpers import safe

class Album:
    'an ordered collection of songs released as a set'
    
    def __init__(self,song):
        self.albumname=song.albumname
        self.safe_name=safe(self.albumname)
        self.year=song.year
        self.copyright=song.copyright
        self.bpm=song.bpm
        self.artist=song.artist
        self.genre=song.genre
        self.composer=song.composer
        self.__artwork=song.artwork()
        self.artwork_filename=self.safe_name+".jpg"
        self.cover_art="PROD_IMAGES"+self.artwork_filename       
        self.albumpage="PROD_ALBUMS"+self.safe_name+".html" 
        self.download_link="PROD_MEDIA"+self.safe_name+".zip"    
        self.__tracks=[]
        self.addSong(song)
        
    def addSong(self,song):
        self.__tracks.append(song)
        self.__tracks.sort(key=lambda x:int(x.track)) 
        
    def artwork(self):
        return self.__artwork
        
    def tracks(self):
        return self.__tracks
     
        