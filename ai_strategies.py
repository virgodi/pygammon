import ai_strategies
import numpy
import copy
import pickle
class SimpleWeights():
    def __init__(self, w, _type=True, name=None):
        # self.score = score
        # self.homed = homed
        # self.alone = alone
        # self.safe = safe
        # self.jailed = jailed
        # self.inhouse = inhouse
        # self.q1 = q1
        # self.q2 = q2
        # self.q3 = q3
        # self.q4 = q4
        # self.aslist = [score, homed, alone, safe, jailed, inhouse, q1, q2, q3, q4]
        self.asList = w
        self.name = name
        self.type = _type
    def copy(self):
        return copy.deepcopy(self)
    def __eq__(self, other):
        if self.asList == other.asList:
            return True
        else:
            return False
    def __str__(self):
        return str(self.name)+': '+str(self.asList)
    def __repr__(self):
        return str(self.name)+': '+str(self.asList)

def score(weights, feature):
    score = 0
    for i in range(len(weights.asList)):
        score += weights.asList[i] * feature[i]
    return score

aggressive = SimpleWeights([1, 1, -2, 0, 10, 2, 3, 2, 1, 0], False, 'Aggressive')
careful = SimpleWeights([1, 1, -5, 0, 1, 3,  4, 3, 0, 0], False, 'Careful')
random_ = SimpleWeights(numpy.random.rand(10), False, 'Random_simple')
logistic = SimpleWeights([  9.62455477,   0.09668296, -27.34340147,  -3.22164878,  -7.27608439,
  -9.72351982,  -0.19527862,  -1.08688916, -1.60798766,  -1.78691726,
  -1.56083934,  -0.26288467,  -0.23365212,  -1.38256598,  -0.98080718,
  -1.62166035, -0.23950076,  -0.0324529,   -2.73831382,  -1.15451162,
  -0.25372656], True, 'logistic')
with open('notebooks_and_data/data/W_long.pkl', 'r') as f:
    logistic_long = SimpleWeights(pickle.load(f)[0], True, 'logistic_long')
with open('notebooks_and_data/data/champs_genetic_41.pkl', 'r') as f:
    genetic_41 = SimpleWeights(pickle.load(f)[-1].asList, True, 'genetic_41')
# genetic_41 = SimpleWeights([9.4379740184713832, -1.591881190331832, -32.414044092735722, -7.8215430111183268, -1.4949528472743272, -8.1386928893443926, 1.5131685052841053, -1.9321123315779674, -3.216231409167797, -0.95493906209830404, -1.311338048050813, 0.6605640547850693, 0.62635861191084019, -2.4484355753599591, 0.44497055798225427, -2.0920587586642574, 3.508256294506118, 2.8764666805501964, 0.23703221331945035, -1.493812558813957, -1.8141502636639406, 0.82875326657381798, -54.573728451094254, -1.4555633351793478, -20.038936587042183, -14.224915333101979, 1.2965373253300716, -4.5716347934649546, -4.8164414785447258, -4.8029787026827897, -3.8958281590120123, -0.19635436641328985, 1.1716163523970726, -2.1167602464343389, -2.1243488791699323, -1.9726429975995077, -1.357179203937771, 0.67218549808109984, -6.5968675560859227, -4.6602156057720183, -0.43427318572197393], True, 'gen41')
with open('notebooks_and_data/data/champs_genetic_21.pkl', 'r') as f:
    genetic_21 = SimpleWeights(pickle.load(f)[-1].asList, True, 'genetic_21')



