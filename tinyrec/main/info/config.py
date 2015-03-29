import ConfigParser
import os 

#get absolute path
directpath = os.getcwd().strip('/').split('/')
for i in range(0,len(directpath))[::-1]:
    if directpath[i] == 'tinyrec':
         directpath = os.path.join("/",*directpath[0:i+1])
         break

config_file_path = os.path.join(directpath,"main/configure")

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class Config(object):
    configdict = {}
    section = ['database','global','dataset'] 
    def __init__(self,cfgpath = config_file_path):
        cfgparser = ConfigParser.ConfigParser()
        cfgparser.readfp(open(cfgpath,"r"))

        for s in self.section:
            self.configdict[s] = {}
            for i in cfgparser.items(s):
                self.configdict[s][i[0]] = i[1]
        self.__type_transformer()
                
    def __type_transformer(self):
        self.__to_type('database','port','int')
        self.__to_type('dataset','maxuserid','int')
        self.__to_type('dataset','maxitemid','int')
        
    def __to_type(self,section,field,totype):
        if totype == "int":
            self.configdict[section][field] = int(self.configdict[section][field])
        elif totype == "float":
            self.configdict[section][field] = float(self.configdict[section][field])
        elif totype == "long":
            self.configdict[section][field] = long(self.configdict[section][field])


    def print_all(self):
        for j in self.configdict:
            print j + ":"
            for k in self.configdict[j]:
                print "\t" + str(k) + " = " + str(self.configdict[j][k])
    
if __name__ == "__main__":
    Config().print_all()


