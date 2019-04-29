#!/bin/bash

FOLDER="ecce/data/"

if [ ! -d "$FOLDER" ]; then
    mkdir "$FOLDER";
fi

cd "$FOLDER"

if [ ! -f ESV.json ]
then
    echo "Downloading ESV..."
    wget https://github.com/honza/bibles/raw/master/ESV/ESV.json
fi

if [ ! -d nave ]
then
    echo "Downloading Nave's Topical Index..."
    wget http://www.justverses.com/downloads/zips/nave.zip
    mkdir nave
    unzip nave.zip -d nave
    rm nave.zip
fi

if [ ! -d tsk ]
then
    echo "Downloading Treasury of Scripture Knowledge..."
    wget http://www.justverses.com/downloads/zips/tsk.zip
    mkdir tsk
    unzip tsk.zip -d tsk
    rm tsk.zip
fi

echo "Downloads finished."
