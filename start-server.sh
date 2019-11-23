#!/bin/bash

VERSION="3.6.8"
PYENV_NAME="ecce_$VERSION"
PORT=${PORT:-8383}

echo $PYENV_NAME > .python-version

echo "Downloading data..."
./download.sh

echo "Setting up python environment..."

if ! command -v pyenv >/dev/null 2>&1; then
    echo "Installing pyenv..."
    curl https://pyenv.run | bash
    exec $SHELL
fi

if ! pyenv versions | grep $VERSION >/dev/null 2>&1; then
    echo "Installing python $VERSION..."
    pyenv install $VERSION
    pyenv rehash
fi

if ! pyenv versions | grep $PYENV_NAME >/dev/null 2>&1; then
    echo "Adding pyenv virtualenv: $PYENV_NAME..."
    pyenv local $VERSION $PYENV_NAME
    pyenv rehash
fi

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Installing server dependency: gunicorn..."
pip install gunicorn

if [ ! -f ./ecce/data/exported/nave-by-reference.json ]; then
   echo "Running nave export..."
   python -m ecce nave-export
fi

if [ ! -f ./ecce/data/exported/verse-with-topics.tsv ]; then
    echo "Running topic export..."
    python -m ecce topic-export
fi

echo "Starting server..."
gunicorn -k uvicorn.workers.UvicornWorker ecce.api.server:app \
         -b 0.0.0.0:$PORT --reload

