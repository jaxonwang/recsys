import similarity

from main.info import config
config.Config().configdict['user-based_CF']['similarity'] = "haha"
config.Config().apply_changes()

y = 2
def a():
    global x,k
    x = 1
def b():
    print x,y

