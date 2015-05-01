import time
from multiprocessing import Process

from main.info import config
#from main.data_structure import vector as vector1
from main.data_structure import sparseVector as vector

user_mean_matrix = {}
def init_user_mean_matrix(dao):
    maxuserid = config.Config().configdict['dataset']['maxuserid']
    for i in range(1,maxuserid + 1):
        m = dao.get_user_rating_mean(i)
        user_mean_matrix[str(i)] = m
    
def to_sparse_vector(vec, vector_len):
    index_list = [i for (i,v) in vec]
    data_list = [v for (i,v) in vec]
    if index_list[-1] >= vector_len:
        raise ValueError("too short length:" + \
                str(vector_len) + " for index :" + str(index_list[-1]))
    return vector.SparseVector(index_list, data_list, vector_len)

#receive two list as vector
def my_sparse_vector_similarity(vectora,vectorb,vec_len):

    sparseveca = to_sparse_vector(vectora,vec_len)
    sparsevecb = to_sparse_vector(vectorb,vec_len)

    startfromone = not startfromzero
    sim = abs(vec_sim(sparseveca,sparsevecb,startfromone))
    if significance_weight:
        i = len(set([i for i,v in vectora]) & set([i for i,v in vectorb]))
        if i < significance_weight:
            sim *= float(i) / float(significance_weight)
    return sim 

def item_based_centralized_vector_similarity(vectora,vectorb,vec_len):
    def centralie_vector(v):
        for i in range(len(v)):
            user_mean = user_mean_matrix[str(v[i][0])]
            v[i] = (v[i][0],v[i][1] - user_mean)

    centralie_vector(vectora)
    centralie_vector(vectorb)
    print vectorb
    sparseveca = to_sparse_vector(vectora,vec_len)
    sparsevecb = to_sparse_vector(vectorb,vec_len)

    startfromone = not startfromzero
    sim = abs(vec_sim(sparseveca,sparsevecb,startfromone))
    return sim 

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
    init_user_mean_matrix(new_DAO_interface())

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


def all_item_similarity():
    '''
    calculate all python similarity and put to the datasore through DAO
    '''

    print "Calculating similarity for each item."
    t1 = time.time()

    init_user_mean_matrix(new_DAO_interface())
    devide_number = multithread
    start = 0 if startfromzero else 1 #whether id start from zero
    total = maxitemid + 1 - start
    proclist = []
    for i in range(0,devide_number):
        end = start + total / 8
        if end > maxitemid or i == devide_number - 1:
            end = maxitemid + 1

        p = Process(target = item_similarity_in_range,args = (start,end))
        proclist.append(p)
        p.start()
        start = end

    for p in proclist:
        p.join()

    t2 = time.time()
    print "All item similarities have been claculated in %ds"%(t2 - t1)

def item_similarity_in_range(start,end):
    dao = new_DAO_interface()

    for itemid in range(start,end):
        simlist = get_other_item_sim(itemid, dao)
        for otheritemid,sim in simlist:
            dao.put_item_sim(itemid,otheritemid,sim)
        #print "User:" + str(userid) + " neighborhood similarity calculated."
        
def get_other_item_sim(itemid, dao):
    '''
    return the similarity between specified item and all other items
    '''
    nearestlist = []
    start = 0 if startfromzero else 1 #whether id start from zero
    item = dao.get_user_list_by_item(itemid)
    if item == []:
        print "No record for %d when calculating item similarity." % (itemid)
        return [] #return a empty list if there are no record for item
    
    for i in range(start,maxitemid + 1):
        if i == itemid:
            continue
        item_i = dao.get_user_list_by_item(i)
        if item_i == []:
            continue    #continue if there are no record for i
        sim = similarity_func(item,item_i,maxuserid + 1)
        if sim != 0.:
            nearestlist.append((i,sim))
    nearestlist.sort(key = lambda nearestlist:nearestlist[1], reverse = True)
    return nearestlist

def clean_all_item_sim():
    print "Clearning previous calculated similarity."
    dao = new_DAO_interface()

    start = 0 if startfromzero else 1 #whether id start from zero
    for itemid in range(start,maxitemid + 1):
        dao.del_item_sim(itemid)
    print "All cleared."


def new_DAO_interface():
    return DAOtype()

def set_config():

    global storetype, similaritytype, maxitemid  
    global maxuserid, startfromzero, multithread 
    global DAOtype, similarity_func, vec_sim, significance_weight, pmodel, all_simlarity

    storetype = config.Config().configdict['global']['storage']
    similaritytype = config.Config().configdict['user_item_CF']['similarity']
    significance_weight= config.Config().configdict['user_item_CF']['significance_weight']
    maxitemid = config.Config().configdict['dataset']['maxitemid'] 
    maxuserid = config.Config().configdict['dataset']['maxuserid'] 
    startfromzero = config.Config().configdict['dataset']['startfromzero'] 
    multithread = config.Config().configdict['global']['multithread'] 
    pmodel = config.Config().configdict['user_item_CF']['model']
    #item-based or user-based
    if pmodel == "user-based":
        all_simlarity = all_user_similarity
    elif pmodel == "item-based":
        all_simlarity = all_item_similarity
    else:
        raise Exception("You should never get here, badly configed.")

    #get the DAO interface
    if storetype == 'redis':
        from main.DAO import redisDAO
        DAOtype = redisDAO.redisDAO

    similarity_func = my_sparse_vector_similarity
    #get the similarity method
    if similaritytype == 'pearson':
        #similarity func must receivce two lists representing vector as [(index,value),...] and a vector length
        vec_sim = vector.pearsonr
    elif similaritytype == 'pearson_intersect':
        vec_sim = vector.pearsonr_hasvalue_both
    elif similaritytype == 'pearson_default':
        vec_sim = vector.pearsonr_default_rate
    elif similaritytype == 'cos':
        vec_sim = vector.cosine
    elif similaritytype == 'spearman':
        vec_sim = vector.spearman
    elif similaritytype == 'adjusted_cos':
        vec_sim = vector.cosine
    else :
        raise Exception("You should never goes into here! Baddly configed.")

set_config()
config.Config().register_function(set_config)

if __name__ == "__main__":
    clean_all_user_sim()

    dao = new_DAO_interface()
    
    t1 = time.time()

    all_user_similarity() 

    t2 = time.time()

    print "Finished in time :",t2 - t1,"s"




