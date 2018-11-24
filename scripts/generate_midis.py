#!/usr/bin/env python

"""
This script generates individual midi files to be used by Aualias' exercises.
The midis are stored in the "midis" folder.
"""

from os import path
from midiutil import MIDIFile


midis_dir = path.realpath('../midis')
track    = 0
channel  = 0
time     = 0    # In beats
duration = 1    # In beats
tempo    = 72   # In BPM
volume   = 127  # 0-127, as per the MIDI standard
major_scale_formula = [0, 2, 2, 1, 2, 2, 2, 1]
major_scale_formula_desc = [0, -1, -2, -2, -2, -1, -2, -2]
major_chord_formula = [0, 4, 3]

# For C4 (degree 60) to C5 (degree 72), generate 1 midi file with 1 note each
for degree in range(60, 73):
	my_midi = MIDIFile(1)
	my_midi.addTempo(track, time, tempo)
	my_midi.addNote(track, channel, degree, time, duration, volume)
	with open("%s/%s.mid" % (midis_dir, degree), "wb") as output_file:
		my_midi.writeFile(output_file)

# Generate all notes of the D major scale
degree = 62
for i, degree_change in enumerate(major_scale_formula):
	degree += degree_change
	my_midi = MIDIFile(1)
	my_midi.addTempo(track, time, tempo)
	my_midi.addNote(track, channel, degree, time, duration, volume)
	with open("%s/%s.mid" % (midis_dir, degree), "wb") as output_file:
		my_midi.writeFile(output_file)

# Generate all notes of the G major scale
degree = 67
for i, degree_change in enumerate(major_scale_formula):
	degree += degree_change
	my_midi = MIDIFile(1)
	my_midi.addTempo(track, time, tempo)
	my_midi.addNote(track, channel, degree, time, duration, volume)
	with open("%s/%s.mid" % (midis_dir, degree), "wb") as output_file:
		my_midi.writeFile(output_file)

# Create the following major chords: C, D, E, F, G, A, B
major_chords = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
major_chords_start_range = [60, 62, 64, 65, 67, 69, 71]
for i, chord in enumerate(major_chords):
	my_midi = MIDIFile(1)
	my_midi.addTempo(track, time, tempo)
	degree = major_chords_start_range[i]
	for degree_change in major_chord_formula:
		degree = degree + degree_change
		my_midi.addNote(track, channel, degree, time, duration, volume)
	with open("%s/%s_major_chord.mid" % (midis_dir, chord), "wb") as output_file:
		my_midi.writeFile(output_file)

# Create all individual notes of F major scale
major_chords = ['f']
major_chords_start_range = [65]
for i, chord in enumerate(major_chords):
	my_midi = MIDIFile(1)
	my_midi.addTempo(track, time, tempo)
	degree = major_chords_start_range[i]
	for i, degree_change in enumerate(major_chord_formula):
		degree = degree + degree_change
		my_midi.addNote(track, channel, degree, i, duration, volume)
	with open("%s/%s-major-chord-individual-notes.mid" % (midis_dir, chord), "wb") as output_file:
		my_midi.writeFile(output_file)

# Create a separate file for each set of notes in D major scale (asc), e.g., D; D & E; D, E, F#; etc.
for h in range(len(major_scale_formula)):
	degree = 62
	my_midi = MIDIFile(1)
	my_midi.addTempo(track, time, tempo)
	for i, degree_change in enumerate(major_scale_formula):
		if i > h:
			break
		degree += degree_change
		my_midi.addNote(track, channel, degree, i, duration, volume)
	with open("%s/scale_d_major_asc_stop_at_%s.mid" % (midis_dir, h), "wb") as output_file:
		my_midi.writeFile(output_file)

# Create a separate file for each set of notes in D major scale (desc)
for h in range(len(major_scale_formula_desc)):
	degree = 74
	my_midi = MIDIFile(1)
	my_midi.addTempo(track, time, tempo)
	for i, degree_change in enumerate(major_scale_formula_desc):
		if i > h:
			break
		degree += degree_change
		my_midi.addNote(track, channel, degree, i, duration, volume)
	with open("%s/scale_d_major_desc_stop_at_%s.mid" % (midis_dir, (7-h)), "wb") as output_file:
		my_midi.writeFile(output_file)

# Create a separate file for each set of notes in F major scale (asc)
for h in range(len(major_scale_formula)):
	degree = 65
	my_midi = MIDIFile(1)
	my_midi.addTempo(track, time, tempo)
	for i, degree_change in enumerate(major_scale_formula):
		if i > h:
			break
		degree += degree_change
		my_midi.addNote(track, channel, degree, i, duration, volume)
	with open("%s/scale_f_major_asc_stop_at_%s.mid" % (midis_dir, h), "wb") as output_file:
		my_midi.writeFile(output_file)

# Create a separate file for each set of notes in F major scale (desc)
for h in range(len(major_scale_formula_desc)):
	degree = 77
	my_midi = MIDIFile(1)
	my_midi.addTempo(track, time, tempo)
	for i, degree_change in enumerate(major_scale_formula_desc):
		if i > h:
			break
		degree += degree_change
		my_midi.addNote(track, channel, degree, i, duration, volume)
	with open("%s/scale_f_major_desc_stop_at_%s.mid" % (midis_dir, (7-h)), "wb") as output_file:
		my_midi.writeFile(output_file)
