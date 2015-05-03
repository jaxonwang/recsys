
import main.core.similarity as sim
from main.info import config

config.Config().configdict['user_item_CF']['model'] = 'item-based'
config.Config().configdict['user_item_CF']['similarity'] = 'adjusted_cos'
config.Config().apply_changes()
dao = sim.new_DAO_interface()
maxuserid = config.Config().configdict['dataset']['maxuserid']

item55 = dao.get_user_list_by_item(55)
item56 = dao.get_user_list_by_item(56)

sim.init_user_mean_matrix(dao)  
print sim.similarity_func(item55,item56,maxuserid + 1)

