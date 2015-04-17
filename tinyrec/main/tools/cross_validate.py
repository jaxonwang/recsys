import main.core.similarity as similarity
import main.core.CFpredictor as CFpredictor
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

    #user similarity
    similarity.all_user_similarity() 

    #RMSE
    rmse = accuracy.RMSE()

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

    rmse_list = []
    for i in range(k_fo):
        train_path = testfile_dir + "/train_%d.dat"%(i)
        test_path = testfile_dir + "/test_%d.dat"%(i)
        config.Config().configdict['dataset']['datafile_path'] = train_path
        config.Config().configdict['dataset']['testfile_path'] = test_path
        config.Config().apply_changes()
        rmse = one_validate()
        rmse_list.append(rmse)
    
    print rmse_list
    print sum(rmse_list)/len(rmse_list)

if __name__ == "__main__":
    cross_validate(6)









