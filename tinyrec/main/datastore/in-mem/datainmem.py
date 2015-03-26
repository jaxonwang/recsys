import sys
import time
sys.path.append('../../tools/datasetreader/')
import datafilereader as RD


# id -> items1,items2.items3 ...
class RatingHashTable:
    table = {}

    def put(self,key,value):
        keystr = str(key)
        if keystr not in self.table:
            self.table[keystr] = []
        self.table[keystr].append(value)

    def get_list_by_id(self,key):
        keystr = str(key)
        return self.table[keystr]

# list[id]= items1,items2.items3 ...
class ArrayListTable:
    table = [None]

    def put(self,key,value):
        while key >= len(self.table):
            self.__double_the_size()
        if self.table[key] is None:
            self.table[key] = []
        self.table[key].append(value)

    def get_list_by_id(self,key):
        return self.table[key]

    def __double_the_size(self):
        for i in range(len(self.table)):
            self.table.append(None)

def benchmark(datastruct):

    t1 = time.clock()
    reader = RD.Reader("../../../../ml-100k/u.data")
    t2 = time.clock()

    it = reader.get_iterator()

    ht = datastruct()

    t3 = time.clock() 
    while True:
        record = it.get_next()
        if record == None:
            break
        #record = [user,movie,rate,time]
        ht.put(record[0],(record[1],record[2])) 

    t4 = time.clock() 
    for i in range(1,943):
        ht.get_list_by_id(i)
    t5 = time.clock()

    print "read     copy     put      get"
    print t2-t1,t3-t2,t4-t3,t5-t4


if __name__ == '__main__':
        
    print "Hashtable"
    benchmark(RatingHashTable)
    print "ArrayListtable"
    benchmark(ArrayListTable)

        
