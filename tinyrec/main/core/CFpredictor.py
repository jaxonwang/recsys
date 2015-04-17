
from main.info import config

def predict_by_knn(dao,userid,itemid):
    sim_list = get_user_topk_neighbor(dao,userid)
    other_user_rate_list = []
    userbaseline = get_Baseline(dao,userid)

    for u,s in sim_list:
        r = dao.get_rate(u,itemid)  #get other users rate
        if r:
            other_user_rate_list.append((u,s,r)) #user, similarity, rate
    if len(other_user_rate_list) == 0:
        #print "No enough information to predict item:%d for user %d."%(itemid,userid)
        #print "return user's baseline rate for the item."
        return userbaseline
    else:
        sum1 = 0.
        sum2 = 0.
        for u,s,r in other_user_rate_list:
            sum1 += s * (r - get_Baseline(dao,u))
            sum2 += s
        predict_rate = userbaseline + sum1 / sum2
        return predict_rate

def get_user_rating_mean(dao, userid):
    rates = dao.get_item_list_by_user(userid)
    total = 0.
    for i,r in rates:
        total += r
    return total / len(rates)
        

def new_DAO_interface():
    return DAOtype()

def get_user_topk_neighbor(dao,userid):
    return dao.get_user_sim_list(userid,neiborsize)

def get_config():
    global CF_config, neiborsize, neibormodel, BP, storetype
    global predict_item_score, get_Baseline, DAOtype

    CF_config = config.Config().configdict['user-based_CF']
    neiborsize = CF_config['neighborsize_k']
    neibormodel = CF_config['neighbormodel']
    BP = CF_config['baseline_predictor']
    storetype = config.Config().configdict['global']['storage']

    #choose function
    if neibormodel == 'knn':
        predict_item_score = predict_by_knn;

    if BP == 'mean':
        get_Baseline = get_user_rating_mean

    if storetype == 'redis':
        from main.DAO import redisDAO
        DAOtype = redisDAO.redisDAO

get_config()
config.Config().register_function(get_config)

if __name__ == "__main__":
    dao = new_DAO_interface()
    for i in range(1,135):
        predict_by_knn(dao,44,i)
