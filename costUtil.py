COST_MAX = 1000.0
def bigramCost(a, b, dict):
	if (a,b) not in dict:
		return COST_MAX
	return 1/(math.log(dict[(a,b)])+1)
