import redis
import sys,os

#get absolute path
directpath = os.getcwd().strip('/').split('/')
for i in range(0,len(directpath))[::-1]:
    if directpath[i] == 'tinyrec':
        sys.path.append(os.path.join("/",*directpath[0:i+1]) + "/main/info")
	break
import config

import numpy as np 
from scipy.sparse import *

######get_config
dbcfg = config.Config().configdict['database']
cfgip = dbcfg['ip']
cfgport = dbcfg['port']
cfgdb = dbcfg['db']

class redisDAO():

    def __init__(self,ip = cfgip,port = cfgport,db=cfgdb):
        self.conn = redis.Redis(ip,port,db)

    def get_item_list_by_user(self,userid):
        return self.conn.hgetall("u" + str(userid))

    def get_user_lsit_by_item(self,itemid):
        return self.conn.hgetall("i" + str(itemid))

    def get_rate(self,userid,itemid):
        return self.conn.hget("u" + str(userid),itemid)

    def get_user_rating_num(self,userid):
	return self.conn.hlen("u" + str(userid))
	
    def get_item_rating_num(self,itemid):
	return self.conn.hlen("i" + str(itemid))

def pearsion_correlation(x,y):

    size = x.shape[1]
    if size == 0 or size != y.shape[1]:
        return
    xm = x.mean()
    ym = y.mean()
    
    Exy = 0.
    Ex = 0.
    Ey = 0.
    Ex2 = 0.
    Ey2 = 0.
    for i in range(size):
        t_x = x[0][i]
        t_y = y[0][i]
        Exy += t_x * t_y
        Ex += t_x
        Ey += t_y
        Ex2 += t_x * t_x
        Ey2 += t_y * t_y
    
    return (Exy - Ex * Ey / size) / np.sqrt((Ex2 - Ex * Ex / size) * (Ey2 - Ey * Ey / size ))

def raw_to_sparse_matrix(raw_record , matrix_len):
    row = np.zeros(len(raw_record))
    col_list = []
    data_list = []
    for k,v in raw_record.items():
        col_list.append(int(k))
        if int(k) >= matrix_len:
            raise ValueError("too short marix length")
        data_list.append(float(v))

    return csr_matrix((data_list,(row,col_list)),shape = (1,matrix_len))

    

if __name__ == "__main__":
	rDAO = redisDAO()
	dscfg = config.Config().configdict['dataset']
        '''
	for i in range(0,dscfg['maxuserid']):
	    rDAO.get_item_list_by_user(i)
	for i in range(0,dscfg['maxitemid']):
	    rDAO.get_user_lsit_by_item(i)
        '''
    
        raw_record_x = rDAO.get_item_list_by_user(44)
        x = raw_to_sparse_matrix(raw_record_x,1683).toarray()

        sim = []
	for i in range(1,dscfg['maxuserid']):
                raw_record_y = rDAO.get_item_list_by_user(i)
                y = raw_to_sparse_matrix(raw_record_y,1683).toarray()
                sim.append((i,pearsion_correlation(x,y)))
        sim.sort(key = lambda sim:sim[1])
