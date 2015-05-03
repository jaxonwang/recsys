import main.DAO.redisDAO as redisDAO

dao = redisDAO.redisDAO()
count = []
for i in range(1,1683):
    a = dao.get_item_sim_list(i,-1)
    if len(a) == 0:
        print i
    else:
        for oi,s in a:
            if s < 1:
                count.append((s,oi,i))
count.sort(reverse = True)
print count[:100]
