LESSONS = {
  "modules": {
    "intervals": {
      "lesson": [
        {
          "title": "Intervals",
          "card_image": "",
          "voice": "An interval is the distance in pitch between two tones. It is labeled by its numerical value and quality.",
          "prompt": "Would you like to learn about the numerical value of an interval?"
        },
        {
          "title": "Intervals - Numerical Value",
          "card_image": "",
          "voice": "The numerical value represents the number of tones included between two notes within a scale.",
          "prompt": "Would you like to hear about the quality of an interval?"
        },
        {
          "title": "Intervals - Quality",
          "card_image": "",
          "voice": "The quality of an interval can be Perfect, Diminished, Augmented, Major, or Minor. Unison, fourth, fifth, and octave are called perfect intervals. Each of them can be diminished (one chromatic tone smaller) or augmented (one chromatic tone larger). The rest of the intervals within an octave are: second, third, sixth and seventh. Each of them can be major or minor.",
          "prompt": "Would you like to hear some example intervals?"
        },
        {
          "title": "Intervals - Perfect Fifth",
          "card_image": "https://s3.amazonaws.com/auralias-alexa-skill/cards/interval_c_major_asc_5.png",
          "voice": "Consider C <audio src=\"https://s3.amazonaws.com/auralias-alexa-skill/mp3s/60.mp3\" /> and G <audio src=\"https://s3.amazonaws.com/auralias-alexa-skill/mp3s/67.mp3\" /> These two notes includes five tones in the C major scale. This is a Perfect Fifth.",
          "prompt": "Would you like to move on to another interval?"
        },
        {
          "title": "Intervals - Diminished Fifth",
          "card_image": "https://s3.amazonaws.com/auralias-alexa-skill/cards/interval_c_major_asc_5_dim.png",
          "voice": "Consider C <audio src=\"https://s3.amazonaws.com/auralias-alexa-skill/mp3s/60.mp3\" /> and G-flat <audio src=\"https://s3.amazonaws.com/auralias-alexa-skill/mp3s/66.mp3\" /> This is a Diminished Perfect Fifth in the C major scale.",
          "prompt": "Would you like to move on to another interval?"
        },
        {
          "title": "Intervals - Augmented Fifth",
          "card_image": "https://s3.amazonaws.com/auralias-alexa-skill/cards/interval_c_major_asc_5_aug.png",
          "voice": "Consider C <audio src=\"https://s3.amazonaws.com/auralias-alexa-skill/mp3s/60.mp3\" /> and G-sharp <audio src=\"https://s3.amazonaws.com/auralias-alexa-skill/mp3s/68.mp3\" /> This is an Augmented Perfect Fifth in the C major scale.",
          "prompt": "Would you like to move on to another interval?"
        },
        {
          "title": "Intervals - Major Third",
          "card_image": "https://s3.amazonaws.com/auralias-alexa-skill/cards/interval_c_major_asc_3.png",
          "voice": "Consider C <audio src=\"https://s3.amazonaws.com/auralias-alexa-skill/mp3s/60.mp3\" /> and E <audio src=\"https://s3.amazonaws.com/auralias-alexa-skill/mp3s/64.mp3\" /> This is an Major Third in the C major scale.",
          "prompt": "Would you like to move on to another interval?"
        },
        {
          "title": "Intervals - Minor Third",
          "card_image": "https://s3.amazonaws.com/auralias-alexa-skill/cards/interval_c_major_asc_3_min.png",
          "voice": "Consider C <audio src=\"https://s3.amazonaws.com/auralias-alexa-skill/mp3s/60.mp3\" /> and E-flat <audio src=\"https://s3.amazonaws.com/auralias-alexa-skill/mp3s/63.mp3\" /> This is a Minor Third in the C major scale.",
          "prompt": "Would you like to assess your knowledge?"
        }
      ],
      "assessment": {
        "title": "Intervals Assessment",
        "instructions": "In this exercise, you will hear two notes in sequence, and if you are using a screen enabled device, you will see the notes. Your goal is to identify the interval between the two notes by name. After I play an interval, say its name by responding unison, major second, major third, perfect fourth, perfect fifth, major sixth, major seventh, or octave. There will be eight questions.",
        "prompt": "Name the interval. For example, octave.",
          "levels": [
            {
              "keys": [
                "c_major"
              ],
              "asc_desc": [
                "asc"
              ],
              "intervals": [
                "unison",
                "major 3rd",
                "perfect 5th",
                "octave"
              ]
            },
            {
              "keys": [
                "c_major"
              ],
              "asc_desc": [
                "asc"
              ],
              "intervals": [
                "unison",
                "major 2nd",
                "major 3rd",
                "perfect 5th",
                "octave"
              ]
            },
            {
              "keys": [
                "c_major"
              ],
              "asc_desc": [
                "asc"
              ],
              "intervals": [
                "unison",
                "major 2nd",
                "major 3rd",
                "perfect 4th",
                "perfect 5th",
                "octave"
              ]
            },
            {
              "keys": [
                "c_major"
              ],
              "asc_desc": [
                "asc"
              ],
              "intervals": [
                "unison",
                "major 2nd",
                "major 3rd",
                "perfect 4th",
                "perfect 5th",
                "major 6th",
                "major 7th",
                "octave"
              ]
            },
            {
              "keys": [
                "c_major"
              ],
              "asc_desc": [
                "desc"
              ],
              "intervals": [
                "unison",
                "major 2nd",
                "major 3rd",
                "perfect 4th",
                "perfect 5th",
                "major 6th",
                "major 7th",
                "octave"
              ]
            }
          ]
      }
    },
    "scales": {
      "lesson": [
        {
          "title": "Scales",
          "card_image": "A scale is a group of notes in succession. The two most common scales are major and minor. Scales are constructed through a formula.",
          "voice": "A scale is a group of notes in succession <audio src=\"https://s3.amazonaws.com/auralias-alexa-skill/mp3s/scale_d_major_asc_stop_at_7.mp3\" /> The two most common scales are major and minor. Scales are constructed through a formula.",
          "prompt": "Would you like to learn how a major scale is constructed?"
        },
        {
          "title": "Scales - Construction",
          "card_image": "https://s3.amazonaws.com/auralias-alexa-skill/cards/scale_construction.png",
          "voice": "Given a starting note, you can determine the major scale with this formula: Whole Step, Whole Step, Half Step, Whole Step, Whole Step, Whole Step, Half Step. A half step is the smallest interval there is. On the piano a half step is one key away from the current note, including black keys. A whole step is comprised of two half steps.",
          "prompt": "Would you like to construct the D major scale?"
        },
        {
          "title": "Scales - D Major",
          "card_image": "https://s3.amazonaws.com/auralias-alexa-skill/cards/scale_d_major_asc.png",
          "voice": "First start with the root note, D, and follow the formula. A whole step from D is E. A whole step from E is F sharp. A half step from F sharp is G. A whole step from G is A. A whole step from A is B. A whole step from B is C sharp. A half step from C sharp is D. The D major scale ends up sounding like this <audio src=\"https://s3.amazonaws.com/auralias-alexa-skill/mp3s/scale_d_major_asc_stop_at_7.mp3\" />",
          "prompt": "Would you like to assess your knowledge?"
        }
      ],
      "assessment": {
        "title": "Scales Assessment",
        "instructions": "In this exercise, if you are using a screen enabled device, you will see the scale. I will play up the scale and randomly stop on a note. Your goal is to tell me the name of the note I stopped on. I will only play the scale within one octave to keep things simple. There will be eight questions.",
        "prompt": "Name the note I stopped on. For example, F sharp.",
        "levels": [
          {
            "keys": [
              "d_major"
            ],
            "asc_desc": [
              "asc"
            ],
            "number_or_note_name": [
              "name"
            ]
          },
          {
            "keys": [
              "d_major"
            ],
            "asc_desc": [
              "desc"
            ],
            "number_or_note_name": [
              "name"
            ]
          }
        ]
      }
    },
    "chords": {
      "lesson": [
        {
          "title": "Chords",
          "card_image": "",
          "voice": "The most basic chords are triads. A triad is a chord constructed of three notes. With the root note on the bottom of the triad (or root position), each note is a third away from the last. There are four types of triads: major, minor, augmented, and diminished.",
          "prompt": "Would you like to hear how a major triad is constructed?"
        },
        {
          "title": "Chords",
          "card_image": "",
          "voice": "To create a major triad, consider a major scale. Stack the first, third, and fifth notes of a major scale on top of each other.",
          "prompt": "Would you like to hear an example?"
        },
        {
          "title": "Chords",
          "card_image": "https://s3.amazonaws.com/auralias-alexa-skill/cards/chord_f_major_construction.png",
          "voice": "With the F major scale <audio src=\"https://s3.amazonaws.com/auralias-alexa-skill/mp3s/scale_f_major_asc_stop_at_7.mp3\" /> take the first, third, and fifth notes of the scale out: F, A, and C <audio src=\"https://s3.amazonaws.com/auralias-alexa-skill/mp3s/f-major-chord-individual-notes.mp3\" /> The F major triad would be F, A, and C <audio src=\"https://s3.amazonaws.com/auralias-alexa-skill/mp3s/f_major_chord.mp3\" />",
          "prompt": "Would you like to assess your knowledge?"
        }
      ],
      "assessment": {
        "title": "Chords Assessment",
        "instructions": "In this exercise, a random major triad will be played, and if you are using a screen enabled device, you will see the triad. Your goal is to identify the triad by name. For example, C major. There will be eight questions.",
        "prompt": "Name the triad. For example, C major.",
        "levels": [
          {
            "chords": [
              "c_major",
              "d_major",
              "f_major",
              "g_major"
            ]
          },
          {
            "chords": [
              "c_major",
              "d_major",
              "e_major",
              "f_major",
              "g_major",
              "a_major",
              "b_major"
            ]
          }
        ]
      }
    }
  }
}