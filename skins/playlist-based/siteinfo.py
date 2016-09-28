#!/usr/bin/env python
import sys

# band info - replace this with your own info
bandname="Geekido Music"
siteroots = {
                'test':"/~chris",
                'design':"/Users/chris/Devel/autobandsite/autobandsite-build",
                'production':"",
            }    
siteowner="Chris Cooke"
showcase_name="Showcase"

# shouldn't need to change anything below this
try:
    siteroot=siteroots[sys.argv[1]]
except:
    siteroot=""