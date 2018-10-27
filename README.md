Auralias
========

Auralias aims to help early stage music students improve their ear training by focusing on traditional learning objectives of ear training but in a setting where the primary interaction with the system will be via voice. Ear training in music education has an overall learning objective of allowing students to develop “a good musical ear” or “musical sensitivity”.

Pre-requisites
------------

* Python 3.7

Installation
------------

Steps to activate the Python virtual environment:

code::

    cd auralias/
    pipenv install
    pipenv shell


Instructions to generate the MP3 files. A dependency is to have a Midi soundfount downloaded and made available in the `midis/midi2mp3.sh` script. In our case, we used a soundfont from https://sites.google.com/site/soundfonts4u/.

code::

    brew install fluidsynth
    brew install lame
    brew install sox
    cd scripts/
    python generate_midis.py
    cd ../midis
    ./midi2mp3.sh *
    mv *.mp3 ../mp3s

To create the skill cards (PNG images), we used LilyPond (http://lilypond.org/) to generate PDFs of the cards. The PDFs were converted to PNG using Mac OS X Preview to prevent quality loss and keep the image size close to a width of 720px.

code::

    cd lilypond_files/
    lilypond-book --output=out --pdf notated_cards.lytex
    find . -name "*-1.pdf" -type f -exec cp {} ./ \;
    # Each PDF was renamed in a consistent way manually.
    # Each PDF was opened in Mac OS X Preview and exported as a PNG where 1" = 520px
    # and saved in the cards/ folder.

Credits
------------

* Midi Python Library: https://pypi.org/project/MIDIUtil/
* Midi to MP3: https://pedrokroger.net/converting-midi-files-mp3-mac-os/
* Soundfount: https://sites.google.com/site/soundfonts4u/
* LilyPond: http://lilypond.org/