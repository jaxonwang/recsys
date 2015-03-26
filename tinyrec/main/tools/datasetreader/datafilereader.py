
class Reader:

        filepath = None
        filehandle = None
        readbuffer = None
        iterator = None

        def __init__(self,filepath):
                self.filepath = filepath
                self.__read_all()
        
        def __read_all(self):
                with open(self.filepath) as self.filehandle:
                        self.readbuffer = self.filehandle.read()

        #define how a record structed
        def record_style(self):
                pass

        def get_iterator(self):
                if self.iterator == None:
                        self.iterator = Iterator(self)
                return self.iterator

class Iterator:

        offset = 0
        bufferlen = None
        rawrecordlist = None

        def __init__(self, reader):
                if reader == None:
                        raise "Reader not initialized."
                self.reader = reader
                self.bufferlen = len(self.reader.readbuffer)
                self.rawrecordlist = self.reader.readbuffer.strip().split("\n")

        def get_all(self):
                return self.reader.get_onle

        #return (user,movie,rate,time)
        def get_next(self):
                if self.rawrecordlist == []:
                        return None
                rawrecord = self.rawrecordlist.pop()
                tmplist = rawrecord.strip().split('\t')
          
                return (int(tmplist[0]),int(tmplist[1]),float(tmplist[2]),int(tmplist[3]))
                
                #no using Record class for performance perpose
                '''
                return Record(tmplist[0],tmplist[1],tmplist[2],tmplist[3]) 
                return Record()
                '''

class Record:

        def __init__(self,user,movie,rate,timestamp):
                self.user = int(user)
                self.movie = int(movie)
                self.rate = float(rate)
                self.timestamp = int(timestamp)
        
        def printrecord(self):
                print "u:%d, m:%d, r:%.1f, t:%d" \
                                % (self.user, self.movie, self.rate, self.timestamp)    
        
if __name__ == "__main__":
        reader = Reader("/Users/chenjunda/wang/recsys/ml-100k/nimabibitest")
        it = reader.get_iterator()
        while True:
                record = it.get_next()
                if record == None:
                        break
                record.printrecord()
        
