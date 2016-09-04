#!/usr/bin/env python
from helpers import safe

class Song:
    'All metadata for a single recording'
        
    def __read_text_tag(self,tag):
        try:
            return self.__tags[tag].text[0]
        except:
            return ''
        
    def __read_data_tag(self,tag):
        try:
            return self.__tags[tag].data
        except:
            return None
                   
    def __init__(self,filename,tags):
        self.filename = safe(filename)
        self.__tags=tags
        self.albumname=self.__read_text_tag('TALB')
        self.albumpage="PROD_ALBUMS"+safe(self.albumname)+".html" 
        self.year=self.__read_text_tag('TDRC').text
        self.track=self.__read_text_tag('TRCK').split('/')[0] 
        self.title=self.__read_text_tag('TIT2')
        self.safe_name=safe(self.albumname)+"_"+safe(self.title)
        self.copyright=self.__read_text_tag('COMM::eng')
        self.bpm=self.__read_text_tag('TBPM')
        self.artist=self.__read_text_tag('TPE1')  
        self.genre=self.__read_text_tag('TCON') 
        self.composer=self.__read_text_tag('TCOM') 
        self.__artwork=self.__read_data_tag('APIC:')
        self.download_link="PROD_MEDIA"+self.filename           
        self.cover_art="PROD_IMAGES"+self.safe_name+".jpg"       
        self.songpage="PROD_SONGS"+self.safe_name+".html"     
        self.grouping=self.__read_text_tag('TIT1')
        self.__groups=[]
        if self.grouping: self.__groups=self.grouping.split(',')
        
    def tags(self):
        return self.__groups
        
    def artwork(self):
        return self.__artwork
        

        

        