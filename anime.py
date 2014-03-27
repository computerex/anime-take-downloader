#!/usr/bin/env python

import re
import urllib
import urllib2
import sys
import os
import subprocess
import time


# execute file with default application
def runfile(filename):
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', filename))
    elif os.name == 'nt':
        os.startfile(filename)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', filename))
        
# this is to removing formatting from the parsed urls
def unescape(s):
    s = s.replace("&amp;", "&")
    # remove the fragment if present
    if "#" in s:
        s = s[:s.find("#")] + s[s.find(";")+1:]
    return s

def downloadfile(link):
    u=urllib2.urlopen(link)
    # to extract the file name
    filename=""
    if "Content-Disposition" in u.info():
        filename = u.info()["Content-Disposition"]
        filename = re.findall("filename=\"(.+?)\"", filename, re.I)[0]
    else:
        # assume we are redirected, get the file name from the base url
        filename = os.path.basename(urllib2.urlparse.urlsplit(u.geturl())[2])
    # check if file exists, return immediately if it does
    if os.path.isfile(filename):
        print("File: " + filename + "\nalready exists")
        return ""
    #urllib.urlretrieve(link, filename)
    f = open(filename, "wb")
    f.write(u.read())
    f.close()
    return filename
class Anime:
    def __init__(self, name, keywords):
        self.name = name
        self.keywords = keywords

class FeedEntry:
    def __init__(self, animeName):
        self.animeName = animeName
        self.downloadLinks = []
               
def main():
    # load the anime list
    animefile = open("anime.txt", "r")
    line = animefile.readline()
    keywords = ""
    animelist = []
    while line != '':
        # read the keyword line
        keywords = animefile.readline()
        if keywords == '':
            print("keywords line empty for anime: " + line)
            return
        # store anime line and keywords
        animelist.append(Anime(line, keywords))
        # read the next anime name line
        line=animefile.readline()
    animefile.close()
    
    # loop
    while True:
        # download feed file
        urllib.urlretrieve("http://feeds.feedburner.com/AnimeTake", "feed.html")
        file = open("feed.html", "r")
        buffer=file.read()
        file.close()

        # delete the feed file
        try:
            os.remove("feed.html")
        except:
            print(sys.exc_info()[0])       
        # parse the first 5 animes in the feed
        buffer=buffer.replace("\n","").replace("\r","").replace("\t","")
        matches=re.findall("<ul class=\"catg_list\">(.+?)</ul>", buffer)
        matches=matches[:5]
        name=""
        mc = 0
        for match in matches:
            # look only for torrent links
            links = re.findall("<li class=\"tor\">(.+?)</li>", match)
            print("MATCH: " + str(mc))
            for link in links:
                    oldlink=link
                    link=link.upper()
                    mismatch=False
                    for anime in animelist:
                            mismatch=False
                            for word in anime.keywords.split():
                                    if word.upper() not in link:
                                            mismatch=True
                                            break
                            if mismatch == False: # that means we have a match
                                    name=anime.name
                                    break
                    if mismatch==False:
                            link=oldlink
                            link=re.findall("<A HREF=\"\s*(.+?)\s*\">",link, re.I)[0]
                            link=unescape(link)       
                            filename=downloadfile(link)                        
                            print(name.rstrip("\n"))
                            print(link)
                            if filename != "":
                              runfile(filename)
                            break
                                                    
            mc=mc+1
        time.sleep(15*60) # check every 15 mins
            
main()
