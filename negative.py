import mtools
import configparser
from re import match
from music21 import converter, analysis, environment
from enum import Enum, unique
import numpy as np
from matplotlib import pyplot as plt
from numpy.core.machar import MachAr
import re

config_file = 'config_files/setting.conf'
config_section_name = 'DEFAULT'

#if __name__ == '__main__':
config = configparser.ConfigParser()
config.read(config_file)
mDictionary = mtools.MDictionaryLoader(config[config_section_name])

s = converter.parse('human_on_score.mxl')
bool_array = [1, 0, 0]

colors = mtools.MArray(["red", "green", "blue"])

analyze_parts_dictionary = {}
ambitusAnalyzer = analysis.discrete.Ambitus()

# print(s.analyze('key'))
# s.remove(s.parts[2])
for part in s.recurse().parts:
    if part.id == 'Analysis':
        analyze_parts_dictionary[part.activeSite.id] = part

for score_id in analyze_parts_dictionary:
    analyze_part = analyze_parts_dictionary[score_id]
    score = analyze_part.activeSite
    pitchMin, pitchMax = ambitusAnalyzer.getPitchSpan(score)
    score.midiRangeCenter = pitchMin.midi + pitchMax.midi
    '''
    for fobj in score.flat.notes:
        if fobj.isNote:
            fobj.pitch.midi=score.midiRangeCenter - fobj.pitch.midi
        elif fobj.isChord:
            for pobj in fobj.pitches:
                pobj.midi = score.midiRangeCenter - pobj.midi 
    '''
    analyze_list = []
    key_record = None
    for note_ in analyze_part.recurse().notes:
        if note_.lyric is not None:
            # if note_.isChord:
            analyze_list.append([note_, note_.getOffsetBySite(score.flat)])
            lyric_ = note_.lyric
            lyric___ = note_.lyric
            note_.lyric = None
            char_index = lyric_.find(': ')
            neb_index = lyric_.find('/')
            neb = None
            if neb_index != -1:
                neb = lyric_[neb_index+1:]
                lyric_ = lyric_[:neb_index]
            if char_index != -1:
                note_.is_key_changed = True
                key_record = lyric_[:char_index]
                lyric_ = lyric_[char_index+2:]
            else:
                note_.is_key_changed = False

            match_ = re.search('\d+', lyric_)
            match_string = ''
            if match_ is not None:
                match_index = match_.start()
                while lyric_[match_index-1] == 'b' or lyric_[match_index-1] == '#':
                    match_index -= 1
                match_string = lyric_[match_index:]
                lyric_ = lyric_[:match_index]
            #note_.addLyric(lyric_)#
            #note_.addLyric(match_string)#
            if neb is not None:
                note_.addLyric(mDictionary.alphabetic_array.getItemByDistance(mDictionary.text_adapter_dictionary[mDictionary.alphabetic_array.getItemByDistance(
                    mDictionary.text_adapter_dictionary[key_record], mDictionary.solmization_array.getIndex(mDictionary.text_adapter_dictionary[neb]))], mDictionary.solmization_array.getIndex(mDictionary.text_adapter_dictionary[lyric_])))
            else:
                note_.addLyric(mDictionary.alphabetic_array.getItemByDistance(
                    mDictionary.text_adapter_dictionary[key_record], mDictionary.solmization_array.getIndex(mDictionary.text_adapter_dictionary[lyric_])))
            note_.addLyric(mDictionary.rome_chord_dictionary[lyric_])
            note_.addLyric(lyric___)
            # note_.lyrics[0].text=note_.quality

    for i in range(len(analyze_list)):
        if i+1 < len(analyze_list):
            analyze_list[i].append(analyze_list[i+1][1])
        else:
            analyze_list[i].append(
                analyze_list[i][0].quarterLength + analyze_list[i][1])
    color_index = 0
    negative_axis = None
    if analyze_list is not None:
        positive_index_by_name = analyze_list[0][0].lyrics[0].text
        negative_index_by_name = mDictionary.alphabetic_array.getItemByDistance(
            positive_index_by_name, mDictionary.chords_dictionary[analyze_list[0][0].lyrics[1].text]['fifth'])
        positive_index = mDictionary.alphabetic_array.getIndex(
            positive_index_by_name)
        negative_index = mDictionary.alphabetic_array.getIndex(
            negative_index_by_name)
        negative_axis = [negative_index_by_name,
                         positive_index_by_name, negative_index, positive_index]
        # print(negative_axis)

    for item in analyze_list:
        pitches_ = []
        # print('----')
        # .getElementsByOffset(item[1],item[2]):
        for note_ in score.recurse().notes:
            offsite___ = note_.getOffsetBySite(score.flat)
            if offsite___ >= item[1] and offsite___ < item[2]:
                note_.style.color = colors[color_index]
                if note_.isNote:
                    pitches_.append(note_.pitch)
                    # note_.pitch.midi+=1
                    # print(note_)
                elif note_.isChord:
                    for note___ in note_:
                        pitches_.append(note___.pitch)
                        # note___.pitch.midi+=1
        item.append(False)  # is V-I 3
        item.append(item[0].lyrics[1].text)  # ModeName 4
        item.append(mDictionary.alphabetic_array.getIndex(
            item[0].lyrics[0].text))  # positiveIndex 5
        item.append(mDictionary.chords_dictionary[item[4]]['negativeModeName'])
        item.append(negative_axis[2]-item[5] -
                    mDictionary.chords_dictionary[item[4]]['fifth']+negative_axis[3])

        # print(item)
        #pitches_ = list(set(pitches_))
        if bool_array[0]:
            for pitch_ in pitches_:
                #midi_12= pitch_.midi%12
                # print('-======')
                # print(pitch_.midi)
                #pitch_.midi+= Mode[item[4]].value['adapter'][midi_12-item[5]]
                # if not hasattr(pitch_, 'hasBeenChanged'):
                # pitch_.hasBeenChanged=True
                midi_12 = pitch_.midi % 12
                pitch_.midi += mDictionary.chords_dictionary[item[4]
                                                             ]['adapter'][midi_12-item[5]]
                move_ = (item[5]-item[7]) % 12
                if move_ < -5:
                    move_ += 12
                elif move_ > 5:
                    move_ -= 12

                pitch_.midi -= move_
                # pitch_.midi+=1
                #    None
                None
                # print(Mode[item[4]].value['adapter'].mlist)
                # print(midi_12)
                # print(pitch_.midi)
                #pitch_.midi-= (item[5]-item[7])%12
            item[0].lyric = None
            item[0].addLyric(mDictionary.alphabetic_array[item[7]])
            item[0].addLyric(item[6])
        elif bool_array[1]:
            is_change = False
            index__ = analyze_list.index(item)
            if index__ < len(analyze_list)-1:

                distance__ = mDictionary.alphabetic_array.getIndex(
                    item[0].lyrics[0].text) - mDictionary.alphabetic_array.getIndex(analyze_list[index__+1][0].lyrics[0].text)
                if distance__ == 7 or distance__ == -5:
                    item[3] = True
                    if index__+2 < len(analyze_list):
                        distance__next = mDictionary.alphabetic_array.getIndex(
                            analyze_list[index__+1][0].lyrics[0].text)-mDictionary.alphabetic_array.getIndex(analyze_list[index__+2][0].lyrics[0].text)
                        if distance__next != 7 and distance__next != -5:
                            is_change = True
                        #is_change = True
                    else:
                        is_change = True

                    for pitch_ in pitches_:
                        item[0].style.color = 'yellow'

            if is_change:
                # print(item)
                for pitch_ in pitches_:
                    midi_12 = pitch_.midi % 12
                    pitch_.midi += mDictionary.chords_dictionary[item[4]
                                                                 ]['adapter'][midi_12-item[5]]
                    if bool_array[2]:
                        pitch_.midi -= 2

                item[0].lyric = None
                if bool_array[2]:
                    item[0].addLyric(mDictionary.alphabetic_array[item[5] - 2])
                else:
                    item[0].addLyric(mDictionary.alphabetic_array[item[5]])
                item[0].addLyric(item[6])
        color_index += 1
    # print(Mode['Ionian'].value['adapter'][101])

    # print(analyze_list)
#environment.set('musicxmlPath', '/usr/bin/musescore3')
s.show()
