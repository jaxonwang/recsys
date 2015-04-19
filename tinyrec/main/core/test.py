import similarity
def func(a,c):
    for i,v in a:
        if i in c:
            print i,v
dao = similarity.new_DAO_interface()
a=dao.get_item_list_by_user(44)
b=dao.get_item_list_by_user(572)

i = set([i for i,v in a]) & set([i for i,v in b])
func(a,i)
print "fuck"
func(b,i)

print similarity.similarity_func(a,b,1682)


