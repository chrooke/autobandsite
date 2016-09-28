#!/usr/bin/env python

# band info - replace this with your own info
bandname="Chris Cooke"
siteroots = {
                'test':"/~chris",
                'design':"/Users/chris/Devel/autobandsite/autobandsite-build",
                'production':"",
            }     
            
# shouldn't need to change anything below this
try:
    siteroot=siteroots[sys.argv[1]]
except:
    siteroot=""