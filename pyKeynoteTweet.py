#!/usr/bin/python
#
# Copyright 2010 Heiko Behrens (http://HeikoBehrens.net)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
'''
Python script to send out tweets while you give a presentation with Keynote.

    usage: ./pyKeynoteTweet.py
    
The script ensures that Keynote runs with exactly one presentation.
On startup it looks at your presenter's notes and lists every tweet it can
find by looking for patterns like

    [twitter]your tweet[/twitter]
    
and warns for tweets that exceed 140 characters. Only in presentation mode
and only once for each slide it sends out tweets using twurl.

For bugs or feature requests visit

    https://github.com/HBehrens/pyKeynoteTweet/issues
'''

from subprocess import call, Popen, PIPE
import getopt
import re
import time
import json
import sys 
try:
    from appscript import *
    import aem
except ImportError:
    sys.exit("ERROR: cannot import appscript. Download and install from http://appscript.sourceforge.net")


info = lambda message: sys.stdout.write(("%s\n" % message).encode('utf-8'))
warn = lambda message: info("WARNING: %s" % message) 

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

# twitter integration
# uses twurl to do actual communication
def ensure_twurl_installed():
    NUL=open('/dev/null', 'w')
    if call("twurl", shell=True, stderr=NUL, stdout=NUL) != 0:
        raise Error("cannot find twurl. Download and install from https://github.com/marcel/twurl")
        
def post_tweet(tweet):
    info("tweeting: %s" % tweet)
    p = Popen("twurl -d 'status=%s' /1/statuses/update.json" % tweet, shell=True, stdout=PIPE)
    result = json.loads(p.communicate()[0].strip())
    if result.has_key("error"):
        warn(result["error"])
        
# keynote integration
# uses appscript/OSA to poll state of keynote     
def tweet_from_slide(slide):
    if not slide.skipped.get():
        m = re.search(r"\[twitter\]\s*(.*?)\s*\[/twitter\]", slide.notes.get())
        if m : return m.group(1)
    return None

def current_keynote_and_slideshow():
    try:
        keynote=app("keynote")
    except aem.findapp.ApplicationNotFoundError:    
        raise Error("keynote is missing on this system. Download and install from http://www.apple.com/iwork/keynote")
       
    if len(keynote.slideshows.get())!=1:
        raise Error("you must have opened exactly one slideshow in keynote")
        
    return (keynote, keynote.slideshows.get()[0])

def validate(slideshow):
    # extra set of validated slides needed to work around strange keynote behavior of skipped slides
    validated_slides = set()
    for slide in slideshow.slides.get():
        slide_id = slide.id.get()
        if slide_id in validated_slides:
            continue
        validated_slides.add(slide_id)
        
        tweet = tweet_from_slide(slide)
        if tweet:
            if len(tweet_from_slide(slide))>140:
                raise Error("tweet to long for slide %d: %s" % (slide.slide_number.get(), tweet_from_slide(slide)))
            info("will tweet(%d): %s" % (slide.slide_number.get(), tweet))
    
def main():
    try:
        (keynote, slideshow)=current_keynote_and_slideshow()
        
        info("working on %s" % slideshow.name.get())
        validate(slideshow)
    
        visited_slides = set()
        while True:
            if keynote.playing.get():
                slide_id = slideshow.current_slide.id.get()
                slide_tweet = tweet_from_slide(slideshow.current_slide) 
                
                if slide_tweet and not slide_id in visited_slides:
                    visited_slides.add(slide_id) 
                    post_tweet(slide_tweet)
                    
            time.sleep(0.5)    
    except:
        sys.exit(sys.exc_info()[1])
    
if __name__ == '__main__':
    main()