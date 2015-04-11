import redis
import sys,os,time

from main.info import config
from main.data_structure import vector

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
        rawdict = self.conn.hgetall("u" + str(userid))
        return [(int(i), float(r)) for (i,r) in rawdict.items()]

    def get_user_lsit_by_item(self,itemid):

        rawdict = self.conn.hgetall("i" + str(itemid))
        return [(int(u), float(r)) for (u,r) in rawdict.items()]

    def get_rate(self,userid,itemid):
        return float(self.conn.hget("u" + str(userid),itemid))

    def get_user_rating_num(self,userid):
	return int(self.conn.hlen("u" + str(userid)))
	
    def get_item_rating_num(self,itemid):
	return (self.conn.hlen("i" + str(itemid)))

    def put_user_nearest(self,userid,otheruser,sim):
        return self.conn.zadd("u_sim_" + str(userid), sim, otheruser)

    def put_item_nearest(self,itemid,otheritem,sim):
        return self.conn.zadd("i_sim_" + str(itemid), sim, otheritem)


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
    #print "Ex",Ex,"Ey",Ey,"Exy",Exy,"Ex2",Ex2,"Ey2",Ey2 
    
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

    
def raw_to_my_sparse_matrix(raw_record , matrix_len):

    col_list = []
    data_list = []
    sortedlist = [(int(k),v) for (k,v) in raw_record.items()]
    sortedlist.sort()

    for k,v in sortedlist:
        col_list.append(int(k))
        if k >= matrix_len:
            raise ValueError("too short marix length")
        data_list.append(float(v))

    return vector.SparseVector(col_list,data_list,matrix_len);

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

        t1 = time.clock()
        x = raw_to_sparse_matrix(raw_record_x,1683).toarray()

        sima = []
	for i in range(1,dscfg['maxuserid']):
                raw_record_y = rDAO.get_item_list_by_user(i)
                y = raw_to_sparse_matrix(raw_record_y,1683).toarray()
                sima.append((i,pearsion_correlation(x,y)))

        t2 = time.clock()
        x = raw_to_my_sparse_matrix(raw_record_x,1683)

        simb = []
	for i in range(1,dscfg['maxuserid']):
                raw_record_y = rDAO.get_item_list_by_user(i)
                y = raw_to_my_sparse_matrix(raw_record_y,1683)
                simb.append((i,vector.pearsonr(x,y)))
        t3 = time.clock()

        print t2 - t1, t3 - t2
        sima.sort(key = lambda sim:sim[1],reverse = True)
        simb.sort(key = lambda sim:sim[1],reverse = True)
        print sima[:200]
        print simb[:200]
