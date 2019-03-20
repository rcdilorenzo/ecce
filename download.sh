#!/bin/bash

FOLDER="ecce/data/"

mkdir "$FOLDER"
cd "$FOLDER"

echo "Downloading ESV..."
wget https://github.com/honza/bibles/raw/master/ESV/ESV.json

echo "Downloading Nave's Topical Index..."
wget http://www.justverses.com/downloads/zips/nave.zip
mkdir nave
unzip nave.zip -d nave
rm nave.zip
