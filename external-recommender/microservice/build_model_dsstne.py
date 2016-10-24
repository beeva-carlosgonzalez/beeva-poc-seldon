

PATH = 'data/recs_10k.tsv'
import re
import sys

def recommendations(recs_path):
    """
    Parse file with user recommendations
    :return:
    """
    with open(recs_path) as f:
        lines = f.readlines()
        fields = map(lambda s:s.rstrip(':\n').split('\t'), lines)

        fields = map(lambda f: (f[0], f[1].split(':')), fields)
        items = map(lambda f: (f[0], map(lambda x: (x.split(',')[0], x.split(',')[1]), f[1])), fields)

        mydict = {key: value for (key, value) in items}
        return mydict


# ## Declare recommender
# By extending class Recommender

# In[14]:

from seldon import Recommender


# In[81]:

class SimpleRecommender(Recommender):

    def __init__(self):
        # Format has to be like
        # self.res = [(1,0.8),(2,0.7)]
        self.res = [(1,0.8),(2,0.7)]
        self.res = recommendations(PATH)

    def recommend(self,user,ids,recent_interactions,client,limit):
        user = str(user)
        if not user in self.res:
            print "user %s not found" %user
            user = self.res.keys()[0]
        return self.res[user][0:limit]


# Save recommender via wrapper

from seldon import Recommender_wrapper


# In[86]:

rr = Recommender_wrapper()
sr1 = SimpleRecommender()
rr.save_recommender(sr1,"dsstne_recommender")

print "Saved dsstne recommender"
