import redis
import sys,os

#get absolute path
directpath = os.getcwd().strip('/').split('/')
for i in range(0,len(directpath))[::-1]:
    if directpath[i] == 'tinyrec':
        sys.path.append(os.path.join("/",*directpath[0:i+1]) + "/main/info")
	break
import config

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

if __name__ == "__main__":
	rDAO = redisDAO()
	dscfg = config.Config().configdict['dataset']
	for i in range(0,dscfg['maxuserid']):
	    rDAO.get_item_list_by_user(i)
	for i in range(0,dscfg['maxitemid']):
	    rDAO.get_user_lsit_by_item(i)

