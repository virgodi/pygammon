class Weights():
	def __init__(self, score, homed, alone, safe, jailed):
		self.score = score
		self.homed = homed
		self.alone = alone
		self.safe = safe
		self.jailed = jailed

def score(weights, feature):
	score = weight.score * feature[0]
	score += weights.home*feature[1]
	score += weights.alone*feature[2]
	score += weights.safe*feature[3]
	score += weights.jailed*feature[4]

aggressive = Weights(1, 1, -2, 0, 5)
careful = Weights(1, 1, -5, 0, 1)