import math
from main.info import config

dao = config.Config().get_dao_instance()

class SparseVector:

    def __init__(self, indices, values, vec_len):
        self.vector_list = []
        self.vector_length = vec_len

        if len(indices) != len(values):
            raise ValueError("Tow list length and vector length do not match.")
        for i in range(len(indices)):
            if indices[i] >= vec_len:
                raise ValueError("Index exceed the vector length.")
            self.vector_list.append((indices[i],values[i]))
        vl = self.vector_list
        vl.sort(key = lambda vl:vl[0])

    def __len__(self):
        return self.vector_length

    def __str__(self):
        s = []
        for i,v in self.vector_list:
            s.append("%d:%.1f\n" % (i,v))
        return "".join(s)

def spearman(sparsevector_a,sparsevector_b,startfromone = False):
    a = []
    b = []

    i,j = 0, 0
    #get the intersection 
    while i < len(sparsevector_a.vector_list) and j < len(sparsevector_b.vector_list):
        index_x, value_x = sparsevector_a.vector_list[i]
        index_y, value_y = sparsevector_b.vector_list[j]

        if index_x > index_y:
            j += 1
        elif index_x < index_y:
            i += 1
        else:
            a.append(value_x)
            b.append(value_y)
            i += 1
            j += 1


    def getrank(vector):
        v = vector[:]
        v.sort()
        v.append(None)#nothing equals to None
        def set_avg(l,start,end):
            avg = (end + start)/2.0 + 1
            for i in range(start,end +1):
                l[i] = avg

        rank_l = range(1,len(v))

        k = 0
        current = v[0]
        for i in range(len(v)):
            if current != v[i]:
                set_avg(rank_l,k,i-1)
                k = i
                current = v[i]
        rdict = {}
        for i in range(len(v)-1):
            rdict[str(v[i])] = rank_l[i]
        return rdict
        
    rank_a = getrank(a)    
    rank_b = getrank(b)    
    #print 'original',a
    #print rank_a
    #print 'original',b
    #print rank_b

    Ex = 0.
    Ey = 0.
    Exy = 0.
    Ex2 = 0.
    Ey2 = 0.

    tmpa = []
    tmpb = []
    for i in range(0,len(a)):
        value_x = rank_a[str(a[i])]
        value_y = rank_b[str(b[i])]
        tmpa.append(value_x)
        tmpb.append(value_y)

        Ey += value_y
        Ey2 += value_y * value_y
        Ex += value_x
        Ex2 += value_x * value_x
        Exy += value_x * value_y
    #print Ex,Ey,Ex2,Ey2,Exy 

    '''
    print tmpa
    print tmpb
    va = SparseVector(range(1,len(tmpa)+1),tmpa,len(tmpa) + 1)
    vb = SparseVector(range(1,len(tmpb)+1),tmpb,len(tmpb) + 1)
    print "pearson", pearsonr(va,vb,True)
    '''
    size = len(a)
    if size >= 1 : 
        lxy = (Ex2 - Ex * Ex / size) * (Ey2 - Ey * Ey / size)
        if lxy != 0:
            sim = (Exy - Ex * Ey / size) / math.sqrt(lxy)
            return sim  
    return 0    #has no correlation


def cosine(sparsevector_a,sparsevector_b,startfromone = False):
    if sparsevector_a.vector_length != sparsevector_b.vector_length:
        raise ValueError("Different vector length.")

    sv_a_m = math.sqrt(sum([v * v for (x,v) in sparsevector_a.vector_list]))
    sv_b_m = math.sqrt(sum([v * v for (x,v) in sparsevector_b.vector_list]))
    dot_product = 0.
    i,j = 0,0
    while i < len(sparsevector_a.vector_list) and j < len(sparsevector_b.vector_list):
        index_x, value_x = sparsevector_a.vector_list[i]
        index_y, value_y = sparsevector_b.vector_list[j]

        if index_x > index_y:
            j += 1
        elif index_x < index_y:
            i += 1
        else:
            dot_product += value_x * value_y
            i += 1
            j += 1

    return dot_product / (sv_a_m * sv_b_m)


def pearsonr(sparsevector_a, sparsevector_b, startfromone = False):
    if sparsevector_a.vector_length != sparsevector_b.vector_length:
        raise ValueError("Different vector length.")
    size = sparsevector_a.vector_length
    if startfromone:
        size -= 1

    Ex = 0.
    Ey = 0.
    Exy = 0.
    Ex2 = 0.
    Ey2 = 0.

    i,j = 0,0
    while i < len(sparsevector_a.vector_list) and j < len(sparsevector_b.vector_list):
        index_x, value_x = sparsevector_a.vector_list[i]
        index_y, value_y = sparsevector_b.vector_list[j]

        if index_x > index_y:
            Ey += value_y
            Ey2 += value_y * value_y
            j += 1
        elif index_x < index_y:
            Ex += value_x
            Ex2 += value_x * value_x
            i += 1
        else:
            Ey += value_y
            Ey2 += value_y * value_y
            Ex += value_x
            Ex2 += value_x * value_x
            Exy += value_x * value_y
            i += 1
            j += 1

    for it in range(i,len(sparsevector_a.vector_list)):
        Ex += value_x
        Ex2 += value_x * value_x
    for it in range(j,len(sparsevector_b.vector_list)):
        Ey += value_y
        Ey2 += value_y * value_y
    '''
    size = i + j
    print "######################33aaa" + str(size)
    '''
    personr = (Exy - Ex * Ey / size) / \
            math.sqrt((Ex2 - Ex * Ex / size) * (Ey2 - Ey * Ey / size))
    return personr


def pearsonr_default_rate(sparsevector_a, sparsevector_b, startfromone = False):
    '''
    if a item is rated by only one user, set the other one rate as zero
    '''
    if sparsevector_a.vector_length != sparsevector_b.vector_length:
        raise ValueError("Different vector length.")

    Ex = 0.
    Ey = 0.
    Exy = 0.
    Ex2 = 0.
    Ey2 = 0.

    i,j = 0,0

    size = 0
    while i < len(sparsevector_a.vector_list) and j < len(sparsevector_b.vector_list):
        index_x, value_x = sparsevector_a.vector_list[i]
        index_y, value_y = sparsevector_b.vector_list[j]

        if index_x > index_y:
            Ey += value_y
            Ey2 += value_y * value_y
            j += 1
        elif index_x < index_y:
            Ex += value_x
            Ex2 += value_x * value_x
            i += 1
        else:
            Ey += value_y
            Ey2 += value_y * value_y
            Ex += value_x
            Ex2 += value_x * value_x
            Exy += value_x * value_y
            i += 1
            j += 1
        size += 1

    for it in range(i,len(sparsevector_a.vector_list)):
        Ex += value_x
        Ex2 += value_x * value_x
        size += 1
    for it in range(j,len(sparsevector_b.vector_list)):
        Ey += value_y
        Ey2 += value_y * value_y
        size += 1

    personr = (Exy - Ex * Ey / size) / \
            math.sqrt((Ex2 - Ex * Ex / size) * (Ey2 - Ey * Ey / size))
    return personr

def pearsonr_hasvalue_both(sparsevector_a, sparsevector_b, startfromone = False):
    '''
    only calculate index which has values both
    '''
    if sparsevector_a.vector_length != sparsevector_b.vector_length:
        raise ValueError("Different vector length.")
    size = sparsevector_a.vector_length
    if startfromone:
        size -= 1

    Ex = 0.
    Ey = 0.
    Exy = 0.
    Ex2 = 0.
    Ey2 = 0.

    i,j = 0,0
    count = 0
    while i < len(sparsevector_a.vector_list) and j < len(sparsevector_b.vector_list):
        index_x, value_x = sparsevector_a.vector_list[i]
        index_y, value_y = sparsevector_b.vector_list[j]

        if index_x > index_y:
            j += 1
        elif index_x < index_y:
            i += 1
        else:
            Ey += value_y
            Ey2 += value_y * value_y
            Ex += value_x
            Ex2 += value_x * value_x
            Exy += value_x * value_y
            i += 1
            j += 1
            count += 1
    size = count

    if size >= 1 : 
        lxy = (Ex2 - Ex * Ex / size) * (Ey2 - Ey * Ey / size)
        if lxy != 0:
            personr = (Exy - Ex * Ey / size) / math.sqrt(lxy)
            return personr
    return 0    #has no correlation




