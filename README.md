# autobandsite
Create a static web site for your music using the metadata in your mp3 files.

Concept: Avoid the security overhead of a dynamic web page by generating a static site from the metadata in the mp3 files. Avoid ALL server-side processing.

Prerequite: The program requires the Mutagen python module. You can find it here: https://bitbucket.org/lazka/mutagen

Usage: 

1. Copy all your mp3 files into the songfiles directory.
2. Copy one of the existing skin directories and edit as desired.
3. Change the skin name in autobandsite.py to the directory name of your skin.
4. In the siteinfo.py for your skin, edit the info as desired.
4. Run autobandsite.py <build target>, where <build target> is one of the site root keys in siteinfo.py.
5. Copy the files from autobandsite-build to your web site.

Warnings: 

- All mp3 files must have an album name and a track number defined.
- Generated site files will not work properly by browsing the files. A web server is required for the site to function properly. 
