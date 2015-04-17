import sys,time
import redis
import main.tools.datasetreader.datafilereader as RD
import main.info.config as config

######get_config
def get_config():
    global dbcfg, cfgip, cfgport, cfgdb, data_path, data_sp, data_ptn
    dbcfg = config.Config().configdict['database']
    cfgip = dbcfg['ip']
    cfgport = dbcfg['port']
    cfgdb = dbcfg['db']
    data_path = config.Config().configdict['dataset']['datafile_path']
    data_sp = config.Config().configdict['dataset']['datafile_seperator']
    data_ptn = config.Config().configdict['dataset']['datafile_pattern']

get_config()
config.Conifg().register_function(get_config)

#################
#db schema:
#1) user to item: hashtable, user:item:rate
#2) item to user: hashtable, item:user:rate

def to_redis(filereader,ip = cfgip,port = cfgport,db=cfgdb):

    reader = RD.Reader(data_path,data_sp,data_ptn)

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

    pipe.execute()
    t2 = time.clock()

    print "Data from %s imported to redis in : %fs" % (data_path, t2 - t1)

if __name__ == "__main__":
    to_redis(RD)


    
