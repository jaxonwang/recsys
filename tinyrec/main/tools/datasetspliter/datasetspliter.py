
from main.tools.datasetreader.datafilereader import *
import random
import StringIO

def split(infile, outdir, k_fo):
    '''
    infile: file to be split
    outdir: folder where the output files go
    k_fo: the number for k fold cross validation

    this funtion will generate k paris of trains and testing data

    '''

    readfile = open(infile,'r')
    #create k test files
    test_files = []
    for i in range(k_fo):
        test_files.append(StringIO.StringIO())
        #test_files.append(open("%s/test_%d.dat"%(outdir,i),"w"))

    #split and write into to k stringIO buffer
    count = 0 
    rating_list_for_a_user = []
    while True:
        line = readfile.readline()
        if not line :
            write_to_file(test_files, rating_list_for_a_user)
            break
        if count % k_fo == 0:
            write_to_file(test_files, rating_list_for_a_user)
            rating_list_for_a_user = []
        rating_list_for_a_user.append(line)
        count += 1
    readfile.close()

    #generate k train and test file pairs
    for i in range(k_fo):
        with open("%s/train_%d.dat"%(outdir,i),"w") as f:
            for j in range(k_fo):
                test_files[j].seek(0)
                if j != i:  #write to file
                    for line in test_files[j]:
                        f.write(line)
        with open("%s/test_%d.dat"%(outdir,i),"w") as f:
            for line in test_files[i]:
                f.write(line)
        
    for f in test_files:
        f.close()
    
def write_to_file(files,l):
    random_permulation(l)
    k = len(files)
    i = 0
    for i in range(len(l)):
        r = l[i]
        files[i].write(r)


def random_permulation(l):
    for i in range(len(l)):
        swap_in_list(l,i,random.randint(i,len(l)-1))

def swap_in_list(l,a,b):
    c = l[a]
    l[a] = l[b]
    l[b] = c

if __name__ == "__main__":
    '''
    #random_permulation_test
    import pprint

    l = range(10)

    d ={}
    count =[]
    for i in range(len(l)):
        count.append([])
        for j in range(len(l)):
            count[i].append(0)

    for i in range(100000):
        l = range(10)
        random_permulation(l)
        for i in range(len(l)):
            count[i][l[i]] += 1

    pprint.pprint(count)
    '''
    #functin test
    split('/home/wjx/recsys/data/ml-100k/u.data','/home/wjx/recsys/data/',10)    


