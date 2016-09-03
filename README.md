# autobandsite
Create a static web site for your music using the metadata in your mp3 files.

Concept: Avoid the security overhead of a dynamic web page by generating a static site from the metadata in the mp3 files. Avoid ALL server-side processing.

Prerequite: The program requires the Mutagen python module. You can find it here: https://bitbucket.org/lazka/mutagen

Usage: 
1) Copy all your mp3 files into the songfiles directory.
2) Copy one of the existing skin directories and edit as desired.
3) Change the skin name in autobandsite.py to the directory name of your skin.
4) Run autobandsite.py
5) Look for an autobandsite-build directory in the parent directory. Copy these files to your web site.

Warnings: 
	- All mp3 files must have an album name and a track number defined.
	- Generated site files will not work properly by browsing the files. 
	  A web server is required for the site to function properly. 
