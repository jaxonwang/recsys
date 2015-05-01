from main.info import config

def set_all_users_mean():
    maxuserid = config.Config().configdict['dataset']['maxuserid']

    dao = config.Config().get_dao_instance()
    for i in range(1,maxuserid + 1):
        item_list = dao.get_item_list_by_user(i)
        ratingsum =sum([r for (x,r) in item_list])
        mean = ratingsum / len(item_list)
        dao.put_user_rating_mean(i,mean)
        
def centralize_user_rate():
    maxuserid = config.Config().configdict['dataset']['maxuserid']

    dao = config.Config().get_dao_instance()
    for u in range(1,maxuserid + 1):
        item_list = dao.get_item_list_by_user(u)
        ratingsum =sum([r for (x,r) in item_list])
        mean = ratingsum / len(item_list)
        for i,r in item_list:
            dao.put_rate(u,i,r - mean)

def preprocess():
    set_all_users_mean()
    if config.Config().configdict['user_item_CF']['similarity'] == 'adjusted_cos':
        centralize_user_rate()
        print "fuck"



