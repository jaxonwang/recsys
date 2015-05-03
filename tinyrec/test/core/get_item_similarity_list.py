
import main.core.similarity as sim
from main.info import config

config.Config().configdict['user_item_CF']['model'] = 'item-based'
config.Config().configdict['user_item_CF']['similarity'] = 'adjusted_cos'
config.Config().apply_changes()
dao = sim.new_DAO_interface()

l = dao.get_item_sim_list(50,-1)

for i,s in l:
    print i,s
