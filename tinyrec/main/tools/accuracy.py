import datasetreader 
import math
import time
import multiprocessing 
import main.core.CFpredictor as CFpredictor
import main.info.config as config
import main.tools.datasetreader.datafilereader as datafilereader


def get_config():
    global seperater, pattern_list, testfilepath
    global multithread
    seperater = config.Config().configdict['dataset']['datafile_seperator']
    pattern_list = config.Config().configdict['dataset']['datafile_pattern']
    testfilepath = config.Config().configdict['dataset']['testfile_path']
    multithread = config.Config().configdict['global']['multithread']

get_config()
config.Config().register_function(get_config)

def RMSE():
    count = 0
    biassquare = 0.
    it = datafilereader.Reader(testfilepath,seperater,pattern_list).get_iterator()
    
    dao = CFpredictor.new_DAO_interface()
    while True:
        record = it.get_next_dict()
        if record == None:
                break
        userid = int(record['user'])
        itemid = int(record['movie'])
        rate = float(record['rate'])
        predict_rate = CFpredictor.predict_item_score(dao,userid,itemid)
        bias = predict_rate - rate
#		print predict_rate,rate
        biassquare += bias * bias
        count += 1

    return math.sqrt(biassquare / count)

def RMSE_multi_process():

    it = datafilereader.Reader(testfilepath,seperater,pattern_list).get_iterator()
    record_list = []
    while True:
        record = it.get_next_dict()
        if record == None:
            break
        record_list.append(record)
    it = None

    def RMSE_multi_subprocess(record_list, start, end, pipe):
        '''
        sub process using shared memery and return bay pipe
        '''
        dao = CFpredictor.new_DAO_interface()

        biassquare = 0.
        for i in range(start,end):
            record = record_list[i]
            userid = int(record['user'])
            itemid = int(record['movie'])
            rate = float(record['rate'])
            predict_rate = CFpredictor.predict_item_score(dao,userid,itemid)
            bias = predict_rate - rate
    #		print predict_rate,rate
            biassquare += bias * bias
        pipe.send(biassquare)

    (p_recv,p_send) = multiprocessing.Pipe(False)
    subprocesses = []
    
    start = 0
    step = len(record_list) / multithread
    for i in range(multithread):
        if i == multithread - 1:
            end = len(record_list)
        else:
            end = start + step
        subproc = multiprocessing.Process(target = RMSE_multi_subprocess,\
                args = (record_list, start, end, p_send))
        subprocesses.append(subproc)
        subproc.start()
        start += step

    total_bias = 0.
    for i in range(multithread):
        tmp = p_recv.recv()
        total_bias += tmp
        subprocesses[i].join()
    
    return math.sqrt(total_bias / len(record_list))


def different_k():
    for i in range(140,65,-5):
        config.Config().configdict['user-based_CF']['neighborsize_k'] = i
        config.Config().apply_changes()
	print RMSE(),i

if __name__ == "__main__":
    #different_k()
    t1 = time.time()
    print RMSE_multi_process()
    t2 = time.time()
    print t2 - t1
