from music21 import converter, analysis, environment, roman
import os
import copy
import re
from re import match


#class for musicpieces, it has functions like getNegativePiece()
class MusicPiece:
    originally_piece = None
    negative_piece = None

    parts_dictionary = {}
    analyze_parts_dictionary = {}
    score_array = []

    is_analyze = False
    is_remove_analysis_part = False

    def __init__(self, pieceFilePath, is_analyze, delete_analysis_part):
        #print(pieceFilePath)
        self.originally_piece = converter.parse(pieceFilePath)
        #print(self.originally_piece)
        self.is_analyze = is_analyze
        self.is_remove_analysis_part = delete_analysis_part

    #Option to analyze and generate romanNumeral part.
    def analyzeNegativePiece(self, mDictionary):
        for score_id in self.parts_dictionary:
            score = self.parts_dictionary[score_id].activeSite
            key_ = analysis.discrete.analyzeStream(score, 'key')
            analysis_part = score.chordify()
            analysis_part.partName = mDictionary.analysis_part_id[0]
            analysis_part.id = mDictionary.analysis_part_id[0]
            score.insert(0, analysis_part)
            is_first = True
            for chord in analysis_part.recurse().getElementsByClass('Chord'):
                chord.closedPosition(forceOctave=4, inPlace=True)
                rn = roman.romanNumeralFromChord(chord, key_)
                if is_first:
                    chord.addLyric(key_.tonicPitchNameWithCase +
                                   ': ' + str(rn.figure))
                    is_first = False
                else:
                    chord.addLyric(str(rn.figure))

    #deepcopy from originally_piece and renew the parts/analyze_parts dictonary
    def renewNegativePiece(self, mDictionary):
        #deepcopy and renew dictionary
        self.negative_piece = copy.deepcopy(self.originally_piece)
        self.parts_dictionary = {}
        self.analyze_parts_dictionary = {}
        self.score_array = []

        if self.is_analyze:
            for part in self.negative_piece.recurse().parts:
                if part.id in mDictionary.analysis_part_id:
                    part.activeSite.remove(part)
                else:
                    self.parts_dictionary[part.activeSite.id] = part
            self.analyzeNegativePiece(mDictionary)

        #find all scores in a stream like {score_id:last part of the score}
        for part in self.negative_piece.recurse().parts:
            self.parts_dictionary[part.activeSite.id] = part
            if part.id in mDictionary.analysis_part_id:
                self.analyze_parts_dictionary[part.activeSite.id] = part

    #change the Rome lyric to chord text
    def anlyzeRome(self, mDictionary):
        if not self.analyze_parts_dictionary:
            print(' Do not have analyze part in this stream.')
            return False
        else:
            #Loop through all of the analyze part score in a stream
            for score_id in self.analyze_parts_dictionary:
                analyze_part = self.analyze_parts_dictionary[score_id]
                score = analyze_part.activeSite
                analyze_array = []
                key_record = None
                #loop through all notes in analyze part
                for note_ in analyze_part.recurse().notes:
                    note_.volume.velocity = 0
                    if note_.lyric is not None:
                        #append lyric Note object and offset to analyze array
                        analyze_array.append(
                            [note_, note_.getOffsetBySite(score.flat)])
                        lyric_ = note_.lyric
                        lyric___ = note_.lyric
                        note_.lyric = None
                        double_ned_index = lyric_.find('//')
                        if double_ned_index != -1:
                            lyric_ = lyric_[:double_ned_index]
                        bracket_l_index = lyric_.find('[')
                        bracket_r_index = lyric_.find(']')
                        if bracket_l_index != -1 and bracket_r_index != -1:
                            lyric_l = lyric_[:bracket_l_index]
                            lyric_r = lyric_[bracket_r_index+1:]
                            lyric_ = lyric_l + lyric_r
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
                        if match_ is not None:
                            match_index = match_.start()
                            while lyric_[match_index-1] == 'b' or lyric_[match_index-1] == '#':
                                match_index -= 1
                            lyric_ = lyric_[:match_index]

                        if neb is not None:
                            note_.addLyric(
                                mDictionary.alphabetic_array.getItemByDistance(
                                    mDictionary.text_adapter_dictionary[
                                        mDictionary.alphabetic_array.getItemByDistance(
                                            mDictionary.text_adapter_dictionary[key_record],
                                            mDictionary.solmization_array.getIndex(
                                                mDictionary.text_adapter_dictionary[neb]
                                            )
                                        )
                                    ],
                                    mDictionary.solmization_array.getIndex(
                                        mDictionary.text_adapter_dictionary[lyric_]
                                    )
                                )
                            )
                        else:
                            note_.addLyric(
                                mDictionary.alphabetic_array.getItemByDistance(
                                    mDictionary.text_adapter_dictionary[key_record],
                                    mDictionary.solmization_array.getIndex(
                                        mDictionary.text_adapter_dictionary[lyric_]
                                    )
                                )
                            )
                        note_.addLyric(
                            mDictionary.rome_chord_dictionary[lyric_])
                        note_.addLyric(lyric___)
                for i in range(len(analyze_array)):
                    if i+1 < len(analyze_array):
                        analyze_array[i].append(analyze_array[i+1][1])
                    else:
                        analyze_array[i].append(
                            analyze_array[i][0].quarterLength + analyze_array[i][1])
                self.score_array.append([score, analyze_array])

    def calculateNegativeIndex(self, mDictionary):
        for score_pair in self.score_array:
            negative_axis = None
            if score_pair[1] is not None:
                positive_index_by_name = score_pair[1][0][0].lyrics[0].text
                negative_index_by_name = mDictionary.alphabetic_array.getItemByDistance(
                    positive_index_by_name, mDictionary.chords_dictionary[score_pair[1][0][0].lyrics[1].text]['fifth'])
                positive_index = mDictionary.alphabetic_array.getIndex(
                    positive_index_by_name)
                negative_index = mDictionary.alphabetic_array.getIndex(
                    negative_index_by_name)
                negative_axis = [negative_index_by_name,
                                 positive_index_by_name, negative_index, positive_index]
            color_index = 0
            for item in score_pair[1]:
                pitches_ = []
                for note_ in score_pair[0].recurse().notes:
                    offsite___ = note_.getOffsetBySite(score_pair[0].flat)
                    if offsite___ >= item[1] and offsite___ < item[2]:
                        note_.style.color = mDictionary.sub_colors[color_index]
                        if note_.isNote:
                            pitches_.append(note_.pitch)
                        elif note_.isChord:
                            for note___ in note_:
                                pitches_.append(note___.pitch)
                item.append(False)  # is V-I 3
                item.append(item[0].lyrics[1].text)  # ModeName 4
                item.append(mDictionary.alphabetic_array.getIndex(
                    item[0].lyrics[0].text))  # positiveIndex 5
                item.append(
                    mDictionary.chords_dictionary[item[4]]['negativeModeName'])
                item.append(negative_axis[2]-item[5] -
                            mDictionary.chords_dictionary[item[4]]['fifth']+negative_axis[3])
                item.append(pitches_)
                color_index += 1

    def NegativePreparation(self, mDictionary):
        self.renewNegativePiece(mDictionary)
        self.anlyzeRome(mDictionary)
        self.calculateNegativeIndex(mDictionary)

    #N modeling
    def NegativePieceByMode_N(self, mDictionary):
        self.renewNegativePiece(mDictionary)
        ambitusAnalyzer = analysis.discrete.Ambitus()

        #Loop through all of the score in a stream
        for score_id in self.parts_dictionary:
            #get score in stream
            score = self.parts_dictionary[score_id].activeSite
            pitchMin, pitchMax = ambitusAnalyzer.getPitchSpan(score)
            score.midiRangeCenter = pitchMin.midi + pitchMax.midi
            for fobj in score.recurse().notes:
                if fobj.isNote:
                    fobj.pitch.midi = score.midiRangeCenter - fobj.pitch.midi
                elif fobj.isChord:
                    for pobj in fobj.pitches:
                        pobj.midi = score.midiRangeCenter - pobj.midi
        return True

    #N+ modeling
    def NegativePieceByMode_N_PLUS(self, mDictionary):
        self.NegativePreparation(mDictionary)
        for score_pair in self.score_array:
            for harmony_part in score_pair[1]:
                for pitch_ in harmony_part[8]:
                    midi_12 = pitch_.midi % 12
                    pitch_.midi += mDictionary.chords_dictionary[harmony_part[4]
                                                                 ]['adapter'][midi_12-harmony_part[5]]
                    move_ = (harmony_part[5]-harmony_part[7]) % 12
                    if move_ < -5:
                        move_ += 12
                    elif move_ > 5:
                        move_ -= 12
                    pitch_.midi -= move_
                harmony_part[0].lyric = None
                harmony_part[0].addLyric(
                    mDictionary.alphabetic_array[harmony_part[7]])
                harmony_part[0].addLyric(harmony_part[6])

    def NegativePieceByMode_N_PLUS_PART(self, mDictionary, type_):
        self.NegativePreparation(mDictionary)
        for score_pair in self.score_array:
            for harmony_part in score_pair[1]:
                is_change = False
                index__ = score_pair[1].index(harmony_part)
                if index__ < len(score_pair[1])-1:

                    distance__ = mDictionary.alphabetic_array.getIndex(
                        harmony_part[0].lyrics[0].text
                    ) - mDictionary.alphabetic_array.getIndex(
                        score_pair[1][index__+1][0].lyrics[0].text)
                    if distance__ == 7 or distance__ == -5:
                        harmony_part[3] = True
                        if index__+2 < len(score_pair[1]):
                            distance__next = mDictionary.alphabetic_array.getIndex(
                                score_pair[1][index__+1][0].lyrics[0].text) - mDictionary.alphabetic_array.getIndex(
                                score_pair[1][index__+2][0].lyrics[0].text)
                            if distance__next != 7 and distance__next != -5:
                                is_change = True
                            #is_change = True
                        else:
                            is_change = True

                        for pitch_ in harmony_part[8]:
                            harmony_part[0].style.color = mDictionary.main_color

                if is_change:
                    # print(harmony_part)
                    for pitch_ in harmony_part[8]:
                        midi_12 = pitch_.midi % 12
                        pitch_.midi += mDictionary.chords_dictionary[harmony_part[4]
                                                                     ]['adapter'][midi_12-harmony_part[5]]
                        if type_ == 'I':
                            pitch_.midi -= 2

                    harmony_part[0].lyric = None
                    if type_ == 'I':
                        harmony_part[0].addLyric(
                            mDictionary.alphabetic_array[harmony_part[5] - 2])
                    else:
                        harmony_part[0].addLyric(
                            mDictionary.alphabetic_array[harmony_part[5]])
                    harmony_part[0].addLyric(harmony_part[6])

    def saveNegativeAsFile(self, mDictionary, savePath, extension):
        if self.is_remove_analysis_part:
            for part in self.negative_piece.recurse().parts:
                if part.id in mDictionary.analysis_part_id:
                    part.activeSite.remove(part)
        self.negative_piece.write(extension, savePath)
