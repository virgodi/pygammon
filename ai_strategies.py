import ai_strategies
import numpy
class SimpleWeights():
    def __init__(self, w, name=None):
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
    def __str__(self):
        return str(self.name)+': '+str(self.asList)
    def __repr__(self):
        return str(self.name)+': '+str(self.asList)

def score(weights, feature):
    score = 0
    for i in range(len(weights.asList)):
        score += weights.asList[i] * feature[i]
    return score

aggressive = SimpleWeights([1, 1, -2, 0, 10, 2, 3, 2, 1, 0], 'Aggressive')
careful = SimpleWeights([1, 1, -5, 0, 1, 3,  4, 3, 0, 0], 'Careful')
random_ = SimpleWeights(numpy.random.rand(10))
custom = SimpleWeights([ 10.50209375, 0.15847234, -26.97449923, -3.73240886, -9.01094207
, -10.21117112, -0.20196128, -1.02301636, -1.728311, -1.69859195,
 -1.49858488, -0.25402805, -0.16265484, -1.4472779, -0.91159558,
 -1.29459407, -0.28702294, -0.06045333, -2.57480468, -1.15007408,
-0.32464122], 'Trained')



