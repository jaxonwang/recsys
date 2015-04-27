import main.core.similarity as sim

dao = sim.new_DAO_interface()

sim.clean_all_item_sim()
print sim.get_other_item_sim(55,dao)
sim.all_item_similarity()
