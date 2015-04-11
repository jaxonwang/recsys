
from main.info import config
from main.data_structure import vector

#receive two list as vector
def my_sparse_vector_pearsonr_similarity(vectora,vectorb,vec_len):
    
    def to_sparse_vector(vec, vector_len):
        index_list = [i for (i,v) in vec]
        data_list = [v for (i,v) in vec]
        if index_list[-1] >= vec_len:
            raise ValueError("too short length:" + \
                    str(vector_len) + " for index :" + str(index_list[-1]))
        return vector.SparseVector(index_list, data_list, vector_len)

    vectora.sort()
    vectorb.sort()

    sparseveca = to_sparse_vector(vectora,vec_len)
    sparsevecb = to_sparse_vector(vectorb,vec_len)

    startfromone = not startfromzero
    return vector.pearsonr(sparseveca,sparsevecb,startfromone)

storetype = config.Config().configdict['global']['storage']
similaritytype = config.Config().configdict['global']['similarity']
maxitemid = config.Config().configdict['dataset']['maxitemid'] 
maxuserid = config.Config().configdict['dataset']['maxuserid'] 
startfromzero = config.Config().configdict['dataset']['startfromzero'] 

#get config
#get the DAO interface
if storetype == 'redis':
    from main.DAO import redisDAO
    DAOtype = redisDAO.redisDAO

#get the similarity method
if similaritytype == 'pearson':
    #similarity func must receivce two lists representing vector as [(index,value),...] and a vector length
    similarity_func = my_sparse_vector_pearsonr_similarity

def get_k_nearest_users(userid):
    '''
return a the k nearest users list in reverse order for a given userid 
these returned ids are searched in the whole user domain
ex get_k_nearest_users(55) -> [(22,0.99),(657,0.96)...]
    '''
    dao = new_DAO_interface()
    nearestlist = []
    start = 0 if startfromzero else 1 #whether id start from zero
    print startfromzero
    user = dao.get_item_list_by_user(userid)
    
    for i in range(start,maxuserid + 1):
        user_i = dao.get_item_list_by_user(i)
        nearestlist.append((i,similarity_func(user,user_i,maxitemid + 1)))
    nearestlist.sort(reverse = True)
    return nearestlist
        
    
def new_DAO_interface():
    return DAOtype()

if __name__ == "__main__":
    dao = new_DAO_interface()

    a = dao.get_item_list_by_user(44)
    b = dao.get_item_list_by_user(57)

    print my_sparse_vector_pearsonr_similarity(a,b,maxitemid+1)

    print get_k_nearest_users(44)
