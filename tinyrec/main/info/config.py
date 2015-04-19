import ConfigParser
import os 
from pprint import *

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
    cfg_validate_matrix = {\
            'global':{\
                    'storage':['redis'],
                    'multithread':'str'},
            'database':{\
                    'ip':       'str',
                    'port':     'int',
                    'db':       'int',
                    'username': 'str or null',
                    'password': 'str or null'},
            'dataset':{\
                    'maxuserid':'int',
                    'maxitemid':'int',
                    'startfromzero':'bool',
                    'datafile_path' :'str',
                    'testfile_path' :'str',
                    'testfile_dir'  :'str',
                    'datafile_seperator':'py_type',
                    'datafile_pattern':'py_type'},
            'user-based_CF':{\
                    'similarity':['pearson','cos','pearson_intersect','pearson_default'],
                    'significance_weight':'int',
                    'neighborsize_k':'int',
                    'neighbormodel' :['knn'],
                    'baseline_predictor':['mean','BP1','BP2','BP3']}
            }

    section = [s for s in cfg_validate_matrix] 
    recall_func_list = []

    def __init__(self,cfgpath = config_file_path):
        cfgparser = ConfigParser.ConfigParser()
        cfgparser.readfp(open(cfgpath,"r"))

        for s in self.section:
            self.configdict[s] = {}
            for i in cfgparser.items(s):
                self.configdict[s][i[0]] = i[1]
        self.config_validater()
        self.set_multi_task_optimize_number()


    def config_validater(self):
        for section in self.cfg_validate_matrix:
            for field in self.cfg_validate_matrix[section]:
                iscfged = field in self.configdict[section] \
                        and self.configdict[section] != ''#existing of section already checked
                ccvm = self.cfg_validate_matrix[section][field]
                if 'null' not in ccvm:#can not be null
                    if not iscfged:
                        raise Exception("field:" + field + " not found in " + section)
                if iscfged:
                    if type(ccvm) == type([]):
                        if self.configdict[section][field] not in ccvm:
                            raise Exception("error config: unknow " + section + ":" + field + " type:" + \
                                    self.configdict[section][field])
                    elif type(ccvm) == type(""):
                        self.__to_type(section,field,ccvm.split(" ")[0])

    #convert original type (string) to specified type
    def __to_type(self,section,field,totype):
        if totype == "int":
            self.configdict[section][field] = int(self.configdict[section][field])
        elif totype == "float":
            self.configdict[section][field] = float(self.configdict[section][field])
        elif totype == "long":
            self.configdict[section][field] = long(self.configdict[section][field])
        elif totype == "bool":
            self.configdict[section][field] = True if self.configdict[section][field] == "True" else False
        elif totype == "py_type":
            raw = self.configdict[section][field]
            exec("pyobj=" + raw)
            self.configdict[section][field] = pyobj

    def register_function(self,func):
        '''
        register function which run depends on the config.
        recall it when config changed.
        '''
        self.recall_func_list.append(func)

    def apply_changes(self):
        for f in self.recall_func_list:
            f()

    def set_multi_task_optimize_number(self):
        get_cpu_num_cmd = "cat /proc/cpuinfo|grep processor |wc -l"
        if self.configdict['global']['multithread'] == 'auto':
            out = os.popen(get_cpu_num_cmd).readlines()[0]
            self.configdict['global']['multithread'] = out
        self.__to_type('global','multithread','int')

    def print_all(self):
        for j in self.configdict:
            print j + ":"
            for k in self.configdict[j]:
                print "\t" + str(k) + " = " + str(self.configdict[j][k])
    
if __name__ == "__main__":
    cfg = Config()
    cfg.print_all()

    pprint(cfg.configdict)


