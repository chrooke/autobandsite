#!/usr/bin/env python
from helpers import safe

class Album:
    'an ordered collection of songs'
    
    def __init__(self,song):
        self.name=song.albumname
        self.albumname=self.name
        self.safe_name=safe(self.name)
        self.year=song.year
        self.copyright=song.copyright
        self.bpm=song.bpm
        self.artist=song.artist
        self.genre=song.genre
        self.composer=song.composer
        self.artwork=song.artwork
        self.artwork_filename=self.safe_name+".jpg"
        self.cover_art="PROD_IMAGES"+self.artwork_filename       
        self.albumpage="PROD_ALBUMS"+self.safe_name+".html" 
        self.download_link="PROD_MEDIA"+self.safe_name+".zip"    
        self.tracks=[]
        self.addSong(song)
        
    def addSong(self,song):
        self.tracks.append(song)
        self.tracks.sort(key=lambda x:int(x.track)) 

        
        