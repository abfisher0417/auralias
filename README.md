Auralias
========

Auralias aims to help early stage music students improve their ear training by focusing on traditional learning objectives of ear training but in a setting where the primary interaction with the system will be via voice. Ear training in music education has an overall learning objective of allowing students to develop “a good musical ear” or “musical sensitivity”.

Pre-requisites
------------

* Python 3.7

Installation
------------

.. code:: python

    brew install fluidsynth

    brew install lame

    brew install sox

    pipenv install

    pipenv shell

    cd scripts

    python generate_midis.py

    cd ../midis

    ./midi2mp3.sh *

    mv *.mp3 ../mp3s

Credits
------------

* 