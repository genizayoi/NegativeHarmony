import csv


#Array for musical objects
class MArray:
    mlist = None

    def __init__(self, item):
        self.mlist = item

    def __getitem__(self, key):
        return self.mlist[key % len(self.mlist)]

    def getIndex(self, item):
        return self.mlist.index(item)

    def getItemByDistance(self, item, distance):
        return self.__getitem__(self.getIndex(item)+distance)


#Return Dictionary objects from 'config_files/*.csv
class MDictionaryLoader:
    alphabetic_array = None
    solmization_array = None
    chords_dictionary = {}
    rome_chord_dictionary = {}
    text_adapter_dictionary = {}

    def __init__(self, config_section):
        self.load_alphabetic_array(config_section['alphabetic_array'])
        self.load_solmization_array(config_section['solmization_array'])
        self.load_chords_dictionary(config_section['chords_dictionary'])
        self.load_rome_chord_dictionary(
            config_section['rome_chord_dictionary'])
        self.load_text_adapter_dictionary(
            config_section['text_adapter_dictionary'])

    def load_alphabetic_array(self, path):
        with open(path, encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                self.alphabetic_array = MArray(row)
        #print(self.alphabetic_array.mlist)

    def load_solmization_array(self, path):
        with open(path, encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                self.solmization_array = MArray(row)
        #print(self.solmization_array.mlist)

    def load_chords_dictionary(self, path):
        with open(path, encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                self.chords_dictionary.update({
                    row[0]:
                    {"fifth": int(row[1]),
                     "negativeModeName": row[2],
                     "adapter": MArray([int(row[3]), int(row[4]), int(row[5]),
                                        int(row[6]), int(row[7]), int(row[8]),
                                        int(row[9]), int(row[10]), int(row[11]),
                                        int(row[12]), int(row[13]), int(row[14])])
                     }}
                )
        #print(self.chords_dictionary)

    def load_rome_chord_dictionary(self, path):
        with open(path, encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                for item in row:
                    self.rome_chord_dictionary.update({item: row[0]})
        #print(self.rome_chord_dictionary)

    def load_text_adapter_dictionary(self, path):
        with open(path, encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                for item in row:
                    self.text_adapter_dictionary.update({item: row[0]})
        #print(self.text_adapter_dictionary)
