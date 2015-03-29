import sys
import time,redis
sys.path.append('../../tools/datasetreader/')
import datafilereader as RD


# id -> items1,items2.items3 ...
class RatingHashTable:
    table = {}

    def __init__(self,**param):
        pass

    def put(self,key,value):
        keystr = str(key)
        if keystr not in self.table:
            self.table[keystr] = []
        self.table[keystr].append(value)

    def get_list_by_id(self,key):
        keystr = str(key)
        return self.table[keystr]

    def commit(self):
        pass

# list[id]= items1,items2.items3 ...
class ArrayListTable:
    table = [None]

    def __init__(self,**param):
        pass

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

    def commit(self):
        pass

class RedisHashTable:

    def __init__(self,**param):

        default = {'host':'127.0.0.1','port':6379,'db':'0'}
        for k in default:
            if k not in param:
                param[k] = default[k]           
        self.host = param['host']
        self.port = param['port']
        self.db = param['db']
        self.__connect()
        
    def __connect(self):
        self.conn = redis.Redis(self.host,self.port,self.db)
        self.pipe = self.conn.pipeline()

    #value is a dict
    def put(self,key,value):
            self.pipe.hset(key,value[0],value[1])

    def commit(self):
        self.pipe.execute()

    def get_list_by_id(self,key):
        return self.conn.hgetall(key)

    def test_clean_all(self):
        self.conn.flushdb()

def benchmark(datastruct,**param):

    t1 = time.clock()
    reader = RD.Reader("../../../../ml-100k/u.data","",['user','movie','rate','time'])
    t2 = time.clock()

    it = reader.get_iterator()

    ht = datastruct()

    t3 = time.clock() 
    #put
    while True:
        record = it.get_next()
        if record == None:
            break
        #record = [user,movie,rate,time]
        ht.put(record[0],(record[1],record[2])) 
    ht.commit()
    #get
    t4 = time.clock() 
    for i in range(1,943):
        ht.get_list_by_id(i)
        
    t5 = time.clock()

    print "read     copy     put      get"
    print t2-t1,t3-t2,t4-t3,t5-t4

    if datastruct == RedisHashTable:
        ht.test_clean_all()
        print 'cleaned'

if __name__ == '__main__':
    print "Hashtable"
    benchmark(RatingHashTable)
    print "ArrayListtable"
    benchmark(ArrayListTable)
    print "RedisHashTable"
    benchmark(RedisHashTable)


        
