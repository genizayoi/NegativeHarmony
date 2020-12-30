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
