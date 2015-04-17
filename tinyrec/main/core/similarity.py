import time
from multiprocessing import Process

from main.info import config
from main.data_structure import vector


def to_sparse_vector(vec, vector_len):
    index_list = [i for (i,v) in vec]
    data_list = [v for (i,v) in vec]
    if index_list[-1] >= vector_len:
        raise ValueError("too short length:" + \
                str(vector_len) + " for index :" + str(index_list[-1]))
    return vector.SparseVector(index_list, data_list, vector_len)

#receive two list as vector
def my_sparse_vector_pearsonr_similarity(vectora,vectorb,vec_len):

    vectora.sort()
    vectorb.sort()

    sparseveca = to_sparse_vector(vectora,vec_len)
    sparsevecb = to_sparse_vector(vectorb,vec_len)

    startfromone = not startfromzero
    return abs(vector.pearsonr(sparseveca,sparsevecb,startfromone))


def set_config():

    global storetype, similaritytype, maxitemid  
    global maxuserid, startfromzero, multithread 
    global DAOtype, similarity_func

    storetype = config.Config().configdict['global']['storage']
    similaritytype = config.Config().configdict['user-based_CF']['similarity']
    maxitemid = config.Config().configdict['dataset']['maxitemid'] 
    maxuserid = config.Config().configdict['dataset']['maxuserid'] 
    startfromzero = config.Config().configdict['dataset']['startfromzero'] 
    multithread = config.Config().configdict['global']['multithread'] 

    #get the DAO interface
    if storetype == 'redis':
        from main.DAO import redisDAO
        DAOtype = redisDAO.redisDAO

    #get the similarity method
    if similaritytype == 'pearson':
        #similarity func must receivce two lists representing vector as [(index,value),...] and a vector length
        similarity_func = my_sparse_vector_pearsonr_similarity
    else :
        print "You should never goes into here! Baddly configed."

set_config()
config.Config().register_function(set_config)

def get_k_nearest_users(userid, dao, k = 200):
    '''
return a the k nearest users list in reverse order for a given userid 
these returned ids are searched in the whole user domain
ex get_k_nearest_users(55) -> [(22,0.99),(657,0.96)...]
    '''
    nearestlist = []
    start = 0 if startfromzero else 1 #whether id start from zero
    user = dao.get_item_list_by_user(userid)
    
    for i in range(start,maxuserid + 1):
        if i == userid:
            continue
        user_i = dao.get_item_list_by_user(i)
        nearestlist.append((i,similarity_func(user,user_i,maxitemid + 1)))
    nearestlist.sort(key = lambda nearestlist:nearestlist[1], reverse = True)
    return nearestlist[:k]

def all_user_similarity():
    '''
    calculate all user similarity and put to the datasore through DAO
    '''

    print "Calculating similarity for each user."
    t1 = time.time()

    devide_number = multithread
    start = 0 if startfromzero else 1 #whether id start from zero
    total = maxuserid + 1 - start
    proclist = []
    for i in range(0,devide_number):
        end = start + total / 8
        if end > maxuserid or i == devide_number - 1:
            end = maxuserid + 1

        p = Process(target = user_similarity_in_range,args = (start,end))
        proclist.append(p)
        p.start()
        start = end

    for p in proclist:
        p.join()

    t2 = time.time()
    print "All user's similarities have been claculated in %ds"%(t2 - t1)

def user_similarity_in_range(start,end):
    dao = new_DAO_interface()

    for userid in range(start,end):
        simlist = get_k_nearest_users(userid, dao)
        for otheruserid,sim in simlist:
            dao.put_user_sim(userid,otheruserid,sim)
        #print "User:" + str(userid) + " neighborhood similarity calculated."

    
def clean_all_user_sim():
    print "Clearning previous calculated similarity."
    dao = new_DAO_interface()

    start = 0 if startfromzero else 1 #whether id start from zero
    for userid in range(start,maxuserid + 1):
        dao.del_user_sim(userid)
    print "All cleared."


def new_DAO_interface():
    return DAOtype()

if __name__ == "__main__":
    clean_all_user_sim()

    dao = new_DAO_interface()
    
    t1 = time.time()

    all_user_similarity() 

    t2 = time.time()

    print "Finished in time :",t2 - t1,"s"




