import main.core.similarity as sim
from main.info import config
config.Config().configdict['user_item_CF']['model'] = 'item-based'
config.Config().configdict['user_item_CF']['similarity'] = 'adjusted_cos'
config.Config().apply_changes()

dao = sim.new_DAO_interface()

sim.init_user_mean_matrix(dao)
sim.get_other_item_sim(313,dao)[:100]

config.Config().configdict['user_item_CF']['similarity'] = 'cos'
config.Config().apply_changes()

print ""
sim.get_other_item_sim(313,dao)[:100]
