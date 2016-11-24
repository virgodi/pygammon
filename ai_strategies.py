import ai_strategies
class Weights():
    def __init__(self, score, homed, alone, safe, jailed, inhouse):
        self.score = score
        self.homed = homed
        self.alone = alone
        self.safe = safe
        self.jailed = jailed
        self.inhouse = inhouse

def score(weights, feature):
    score = weights.score * feature[0]
    score += weights.homed*feature[1]
    score += weights.alone*feature[2]
    score += weights.safe*feature[3]
    score += weights.jailed*feature[4]
    score += weights.inhouse*feature[5]
    return score

aggressive = Weights(1, 1, -2, 0, 10, 2)
careful = Weights(1, 1, -5, 0, 1, 3)

