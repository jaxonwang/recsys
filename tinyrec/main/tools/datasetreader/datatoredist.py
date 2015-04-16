import sys,time
import redis
sys.path.append('../../tools/datasetreader/')
sys.path.append("../../info/")
import datafilereader as RD
import config 

######get_config
dbcfg = config.Config().configdict['database']
cfgip = dbcfg['ip']
cfgport = dbcfg['port']
cfgdb = dbcfg['db']

#################
#db schema:
#1) user to item: hashtable, user:item:rate
#2) item to user: hashtable, item:user:rate

def to_redis(filereader,ip = cfgip,port = cfgport,db=cfgdb):

    reader = RD.Reader("../../../../ml-100k/u.data","\t",['user','movie','rate','time'])

    it = reader.get_iterator()

    conn = redis.Redis(ip,port,db)
    pipe = conn.pipeline()

    t1 = time.clock()
    while True:
        record = it.get_next_dict()
        if record == None:
            break
        pipe.hset("u"+str(record["user"]),record['movie'],record['rate'])
        pipe.hset("i"+str(record["movie"]),record['user'],record['rate'])

    t2 = time.clock()
    pipe.execute()
    t3 = time.clock()

    print t2 - t1,t3 - t2

if __name__ == "__main__":
    to_redis(RD)


    
