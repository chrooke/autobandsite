# autobandsite
Create a static web site for your music using the metadata in your mp3 files.

Concept: Avoid the security overhead of a dynamic web page by generating a static site from the metadata in the mp3 files. Avoid ALL server-side processing.

Prerequite: The program requires the Mutagen python module. You can find it here: https://bitbucket.org/lazka/mutagen

Usage: copy all your mp3 files into the songfiles directory, then run the script. Look for an autobandsite-build directory in the parent directory. Copy these files to your web site.

Assumptions: all mp3 files must have an album name and a track number defined.
