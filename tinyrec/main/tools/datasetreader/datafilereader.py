#this python script is to read the data from file to memory, and provied a itorater to retrive them.
class Reader:

        filepath = None
        filehandle = None
        readbuffer = None
        iterator = None
        separator = None  #how to get a record and how a record is organized. Used for find a record
        fieldname = None #the name for each field of a record, strored as a list

        def __init__(self,filepath,separator,fieldname):
                self.filepath = filepath
                self.__read_all()
                self.separator = separator
                self.fieldname = fieldname[:]
        
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

        #Using the separator described in Reader, and return a tuple according to the filed name list. 
        def get_next_dict(self):
                if self.rawrecordlist == []:
                        return None
                rawrecord = self.rawrecordlist.pop()
                tmplist = rawrecord.strip().split(self.reader.separator)
          
                retdict = {}
                for i in range(0,len(tmplist)):
                    retdict[self.reader.fieldname[i]] = tmplist[i]

                return retdict
                

        def get_next(self):
                if self.rawrecordlist == []:
                        return None
                rawrecord = self.rawrecordlist.pop()
                tmplist = rawrecord.strip().split(self.reader.separator)
          
                return tmplist
                

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
        reader = Reader("/home/wjx/recsys/ml-1m/ratings.dat","::",['user','movie','rate','time'])
        it = reader.get_iterator()
        while True:
                record = it.get_next_dict()
                if record == None:
                        break
                print record

