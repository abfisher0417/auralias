#!/usr/bin/env bash
# fluidsynth -F output.wav ~/Soundfonts/my-soundfont.sf2 myfile.midi
# lame output.wav output.mp3 -b 48
# soxi output.mp3 

SOUNDFONT=/Users/andrewfisher/Devel/auralias/soundfont/Sal-Stein-Uprights-Detailed-V3.0.sf2

if [[ ! -f $SOUNDFONT ]]
then
    echo "Couldn't find the soundfont: $SOUNDFONT"
    exit 1
fi


if [ "$#" -eq 0 ]
then
    echo "usage: midi2mp3 file1.mid [file2.mid, file3.mid, ...]"
    exit 0
else
    for filename in "$@"
    do
        echo "${filename}"
        WAVFILE="${filename%.*}"

        fluidsynth -F "${WAVFILE}" $SOUNDFONT "${filename}" && \
            lame "${WAVFILE}" -b 48 && \
            rm "${WAVFILE}"
    done
fi