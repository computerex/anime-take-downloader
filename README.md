anime-take-downloader
=====================

A simple python script for automatically downloading files from Anime Take feed
Works with Python 2.7. Anime.txt file contains on one line the name of the anime
followed by keywords for matching against the different sources. 

example:

Servant x Service

[HorribleSubs] Servant x Service 1080p


The name of the anime is "Servant x Service" 
The script will only attempt to download the torrent
file from [HorribleSubs] and one that is 1080p. You 
can make the second line less specific if you want,
and it'll download the first source it matches against. 


