#!/usr/bin/env bash
rm data/ang2011.xml
#wget http://www.talk910.com/podcast/ang2011.xml 
wget http://www.kste.com/podcast/armandgettypodcast.xml
mv ang2011.xml data/
rm episodes.db 
cp ../episodes.db . 
python provision-data.py
cp episodes.db ../