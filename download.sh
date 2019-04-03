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

if [ ! -d glove ]
then
    echo "Downloading 'globe.42B.300d.zip' for word embeddings..."
    wget http://nlp.stanford.edu/data/glove.42B.300d.zip
    unzip glove.42B.300d.zip -d glove
    rm glove.42B.300d.zip
fi

echo "Downloads finished."
