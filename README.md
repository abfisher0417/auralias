Auralias
========

Auralias aims to help early stage music students improve their ear training by focusing on traditional learning objectives of ear training but in a setting where the primary interaction with the system will be via voice. Ear training in music education has an overall learning objective of allowing students to develop “a good musical ear” or “musical sensitivity”.

Pre-requisites
------------

* Python 3.7
* Python 2.7

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

    # Increase the gain of all generated audio files using sox
    for file in ./*.mp3
    do
        sox $file ./$file gain -n -10
    done

    # Format all MP3s to have 48k bit rate and 16k sample rate
    for file in ./*.mp3
    do
        ~/ffmpeg -i $file -ac 2 -codec:a libmp3lame -b:a 48k -ar 16000 ./$file
    done

To create the skill cards (PNG images), we used LilyPond (http://lilypond.org/) to generate PDFs of the cards. The PDFs were converted to PNG using Mac OS X Preview to prevent quality loss and keep the image size close to a width of 720px.

code::

    cd lilypond_files/
    lilypond-book --output=out --pdf notated_cards.lytex
    find . -name "*-1.pdf" -type f -exec cp {} ./ \;
    # Each PDF was renamed in a consistent way manually.
    # Each PDF was opened in Mac OS X Preview and exported as a PNG where 1" = 520px
    # and saved in the cards/ folder.

# AWS S3 bucket

The folders cards and mp3s must be uploaded to an AWS S3 bucket with public read access granted to all folders/files.

A CORS configuration must be specified on the bucket:

code::

    <?xml version="1.0" encoding="UTF-8"?>
    <CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
    <CORSRule>
        <AllowedOrigin>http://ask-ifr-download.s3.amazonaws.com</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
    </CORSRule>
    <CORSRule>
        <AllowedOrigin>https://ask-ifr-download.s3.amazonaws.com</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
    </CORSRule>
    </CORSConfiguration>


# AWS DynamoDB

DynamoDB is automatically initialized when the skill runs in AWS Lambda.

# AWS Lambda

An AWS Lambda function auraliasMusic must be created. It is based on Python 2.7.

code::

    cd lambda
    pip install -r py/requirements.txt -t skill_env
    cp -r py/* skill_env/
    cd skill_env/
    zip -r skill_env.zip *

Upload the skill_env.zip file to your AWS Lambda function.

Credits
------------

* Midi Python Library: https://pypi.org/project/MIDIUtil/
* Midi to MP3: https://pedrokroger.net/converting-midi-files-mp3-mac-os/
* Soundfount: https://sites.google.com/site/soundfonts4u/
* LilyPond: http://lilypond.org/
* Alexa Skill Sample: https://github.com/alexa/skill-sample-python-highlowgame/tree/master/instructions