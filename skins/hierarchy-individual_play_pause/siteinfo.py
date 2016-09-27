#!/usr/bin/env python

# band info - replace this with your own info
bandname="Chris Cooke"
siteroots = {
                'test':"/~chris",
                'production':"",
            }  
            
# should need to change anything below this
try:
    siteroot=siteroots[sys.argv[1]]
except:
    siteroot=""