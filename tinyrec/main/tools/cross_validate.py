import main.core.similarity as similarity
import main.core.CFpredictor as CFpredictor
import main.core.preprocess as preprocess
import main.tools.datasetreader.datatoredis as  datatoredis
import main.tools.accuracy as accuracy
import main.tools.datasetspliter.datasetspliter as datasetspliter
import main.info.config as config
import time

def one_userbased_CF_validate():
    dao = similarity.new_DAO_interface()
    dao.del_all_keys()
    print "all keys cleared."

    #read in file 
    datatoredis.to_redis()

    #preproces
    preprocess.preprocess()

    #similarity, user/item determinded by config
    similarity.all_simlarity() 

    #RMSE
    rmse = accuracy.RMSE_MAE()

    return rmse

def get_config():
    global one_validate, datafile_path, testfile_dir
    one_validate = one_userbased_CF_validate
    datafile_path = config.Config().configdict['dataset']['datafile_path']
    testfile_dir = config.Config().configdict['dataset']['testfile_dir']


get_config()
config.Config().register_function(get_config)

def cross_validate(k_fo):
    datasetspliter.split(datafile_path,testfile_dir,k_fo)

    rmse_mae_list = []
    for i in range(k_fo):
        train_path = testfile_dir + "/train_%d.dat"%(i)
        test_path = testfile_dir + "/test_%d.dat"%(i)
        config.Config().configdict['dataset']['datafile_path'] = train_path
        config.Config().configdict['dataset']['testfile_path'] = test_path
        config.Config().apply_changes()
        accu = one_validate()
        rmse_mae_list.append(accu)
    
    print rmse_mae_list
    print sum([x for x,y in rmse_mae_list])/len(rmse_mae_list),\
            sum([y for x,y in rmse_mae_list]/len(rmse_mae_list))

if __name__ == "__main__":
    #cross_validate(6)
    #print one_userbased_CF_validate()
    '''
    config.Config().configdict['user_item_CF']['similarity'] = 'pearson'

    '''
    '''
    for i in range (1,250,5):
        config.Config().configdict['user_item_CF']['significance_weight'] = i
        config.Config().apply_changes()
        print one_userbased_CF_validate(),i
    #print similarity.get_k_nearest_users(688,similarity.new_DAO_interface())
    config.Config().configdict['user_item_CF']['similarity'] = 'pearson' 
    config.Config().apply_changes()
    print one_userbased_CF_validate()
    '''

    config.Config().configdict['user_item_CF']['model'] = 'item-based' 
    config.Config().configdict['user_item_CF']['similarity'] = 'adjusted_cos' 
    config.Config().apply_changes()
    print one_userbased_CF_validate()

    '''
    config.Config().configdict['user_item_CF']['model'] = 'item-based' 
    config.Config().configdict['user_item_CF']['similarity'] = 'cos' 
    config.Config().apply_changes()
    print one_userbased_CF_validate()

    config.Config().configdict['user_item_CF']['similarity'] = 'cos' 
    config.Config().apply_changes()
    print one_userbased_CF_validate()

    config.Config().configdict['user_item_CF']['similarity'] = 'spearman' 
    config.Config().apply_changes()
    print one_userbased_CF_validate()
    '''
    '''
    dao = similarity.new_DAO_interface()
    a=dao.get_item_list_by_user(688)
    b=dao.get_item_list_by_user(598)
    print similarity.similarity_func(a,b,1682)
    '''










