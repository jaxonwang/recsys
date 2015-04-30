import main.DAO.redisDAO as redisDAO

dao = redisDAO.redisDAO()
count = []
for i in range(1,1683):
    a = dao.get_item_sim_list(i,-1)
    if len(a) == 0:
        print i
    else:
        for i,s in a:
            count.append(s)
count.sort(reverse = True)
tmp = []
for i in range(0,len(count),2):
    tmp.append(count[i])
for i in tmp:
    print i

