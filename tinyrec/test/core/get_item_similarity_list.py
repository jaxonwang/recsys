
import main.core.similarity as sim
from main.info import config

config.Config().configdict['user_item_CF']['model'] = 'item-based'
config.Config().configdict['user_item_CF']['similarity'] = 'adjusted_cos'
config.Config().apply_changes()
dao = sim.new_DAO_interface()

maxitemid = config.Config().configdict['dataset']['maxitemid']
maxuserid = config.Config().configdict['dataset']['maxuserid']
sim.init_user_mean_matrix(dao)  

ri = 50
ril = dao.get_user_list_by_item(ri)
l = []
for i in range(1,maxitemid + 1):
    il = dao.get_user_list_by_item(i)
    if il == []:
        continue
    sima = sim.similarity_func(ril,il,maxuserid + 1)
    l.append((i,sima))

for i,s in l:
    print i,s
