
import redisDAO

def func(a,c):
    for i,v in a:
        if i in c:
            print i,v

dao = redisDAO.redisDAO()

a = dao.get_item_list_by_user(44)
a.sort()
b = dao.get_item_list_by_user(572)
b.sort()

c = set([i for i,v in a])&set([i for i,v in b])
func(a,c)
print "fuck"
func(b,c)

print "user",a
print "user",b
print "sim",dao.get_user_sim_list(44,50)
