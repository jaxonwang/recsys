import redis
import sys,os,time

from main.info import config


######get_config
def get_config():
    global dbcfg, cfgip, cfgport, cfgdb
    dbcfg = config.Config().configdict['database']
    cfgip = dbcfg['ip']
    cfgport = dbcfg['port']
    cfgdb = dbcfg['db']

get_config()
config.Config().register_function(get_config)

class redisDAO():

    def __init__(self,ip = cfgip,port = cfgport,db=cfgdb):
        self.conn = redis.Redis(ip,port,db)

    def put_user_rate(self,userid,itemid,rating):
        return self.conn.hset("u" + str(userid),itemid,rating)
          
    def put_item_rate(self,itemid,userid,rating):
        return self.conn.hset("i" + str(itemid),userid,rating)

    def get_item_list_by_user(self,userid):
        rawdict = self.conn.hgetall("u" + str(userid))
        retlist = []
        for (i,r) in rawdict.items():
            if i[0] >= '0' and i[0] <= '9': #only append item and ratings
                retlist.append((int(i),float(r)))
        return retlist

    def get_user_list_by_item(self,itemid):
        rawdict = self.conn.hgetall("i" + str(itemid))
        return [(int(u), float(r)) for (u,r) in rawdict.items()]

    def get_rate(self,userid,itemid):

        ret = self.conn.hget("u" + str(userid),itemid)
        if ret:     #record exist
            return float(ret)
        return ret

    def get_user_rating_num(self,userid):
	return int(self.conn.hlen("u" + str(userid)))
	
    def get_item_rating_num(self,itemid):
	return (self.conn.hlen("i" + str(itemid)))

    def put_user_sim(self,userid,otheruser,sim):
        return self.conn.zadd("u_sim_" + str(userid), otheruser, sim)

    def get_user_sim_list(self,userid,k,bydesc = True):
        l = self.conn.zrange("u_sim_" + str(userid), 0, k, \
                desc = bydesc, withscores = True)
        l =[(int(i), sim) for (i, sim) in l]
        return l

    def put_item_sim(self,itemid,otheritem,sim):
        return self.conn.zadd("i_sim_" + str(itemid), otheritem, sim)

    def get_item_sim_list(self,itemid,k,bydesc = True):
        l = self.conn.zrange("i_sim_" + str(itemid), 0, k, \
                desc = bydesc, withscores = True)
        l =[(int(i), sim) for (i, sim) in l]
        return l

    def get_sim_between_two_items(self,itemaid,itembid):
        sim = self.conn.zscore("i_sim_" + str(itemaid), itembid)
        if sim:
            return float(sim)
        return 0

    def put_user_rating_mean(self,userid,meanvalue):
        return self.conn.hset("u" + str(userid),"mean",meanvalue)
    
    def get_user_rating_mean(self,userid):
        mean = self.conn.hget("u" + str(userid), "mean")
        if mean:
            return float(mean)
        else:
            return 0.

    def del_user_sim(self,userid):
        return self.conn.delete("u_sim_" + str(userid))

    def del_item_sim(self,itemid):
        return self.conn.delete("i_sim_" + str(itemid))

    def del_all_keys(self):
        return self.conn.flushdb()



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

    

if __name__ == "__main__":
	rDAO = redisDAO()
	dscfg = config.Config().configdict['dataset']
        '''
	for i in range(0,dscfg['maxuserid']):
	    rDAO.get_item_list_by_user(i)
	for i in range(0,dscfg['maxitemid']):
	    rDAO.get_user_lsit_by_item(i)
    
        raw_record_x = rDAO.get_item_list_by_user(44)

        t1 = time.clock()
        x = raw_to_sparse_matrix(raw_record_x,1683).toarray()

        sima = []
	for i in range(1,dscfg['maxuserid']):
                raw_record_y = rDAO.get_item_list_by_user(i)
                y = raw_to_sparse_matrix(raw_record_y,1683).toarray()
                sima.append((i,pearsion_correlation(x,y)))

        t2 = time.clock()
        sima.sort(key = lambda sim:sim[1],reverse = True)
        print sima[:200]
        '''
        print rDAO.get_user_sim_list(44,111) 

