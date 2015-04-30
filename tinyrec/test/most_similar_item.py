import main.DAO.redisDAO as redisDAO

dao = redisDAO.redisDAO()
count = []
for i in range(1,1683):
    a = dao.get_item_sim_list(i,0)
    if len(a) == 0:
        print i
    else:
        count.append((i,a[0][0],a[0][1]))
count.sort(key =lambda count:count[2])
print count


