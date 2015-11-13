import heapq, collections, re, sys, time, os, random, math
from ppp_main import PaperPlusPlus

############################################################
# Abstract interfaces for search problems and search algorithms.

SENTENCE_BEGIN = '-BEGIN-'

class SearchProblem:
	# Return the start state.
	def startState(self): raise NotImplementedError("Override me")

	# Return whether |state| is a goal state or not.
	def isGoal(self, state): raise NotImplementedError("Override me")

	# Return a list of (action, newState, cost) tuples corresponding to edges
	# coming out of |state|.
	def succAndCost(self, state): raise NotImplementedError("Override me")

class SearchAlgorithm:
	# First, call solve on the desired SearchProblem |problem|.
	# Then it should set two things:
	# - self.actions: list of actions that takes one from the start state to a goal
	#                 state; if no action sequence exists, set it to None.
	# - self.totalCost: the sum of the costs along the path or None if no valid
	#                   action sequence exists.
	def solve(self, problem): raise NotImplementedError("Override me")

############################################################
# Uniform cost search algorithm (Dijkstra's algorithm).

class UniformCostSearch(SearchAlgorithm):
	def __init__(self, verbose=0):
		self.verbose = verbose

	def solve(self, problem):
		# If a path exists, set |actions| and |totalCost| accordingly.
		# Otherwise, leave them as None.
		self.actions = None
		self.totalCost = None
		self.numStatesExplored = 0

		# Initialize data structures
		frontier = PriorityQueue()  # Explored states are maintained by the frontier.
		backpointers = {}  # map state to (action, previous state)

		# Add the start state
		startState = problem.startState()
		frontier.update(startState, 0)

		while True:
			# Remove the state from the queue with the lowest pastCost
			# (priority).
			state, pastCost = frontier.removeMin()
			if state == None: break
			self.numStatesExplored += 1
			if self.verbose >= 2:
				print "Exploring %s with pastCost %s" % (state, pastCost)

			# Check if we've reached the goal; if so, extract solution
			if problem.isGoal(state):
				self.actions = []
				while state != startState:
					action, prevState = backpointers[state]
					self.actions.append(action)
					state = prevState
				self.actions.reverse()
				self.totalCost = pastCost
				if self.verbose >= 1:
					print "numStatesExplored = %d" % self.numStatesExplored
					print "totalCost = %s" % self.totalCost
					print "actions = %s" % self.actions
				return

			# Expand from |state| to new successor states,
			# updating the frontier with each newState.
			for action, newState, cost in problem.succAndCost(state):
				if self.verbose >= 3:
					print "  Action %s => %s with cost %s + %s" % (action, newState, pastCost, cost)
				if frontier.update(newState, pastCost + cost):
					# Found better way to go to |newState|, update backpointer.
					backpointers[newState] = (action, state)
		if self.verbose >= 1:
			print "No path found"

# Data structure for supporting uniform cost search.
class PriorityQueue:
	def  __init__(self):
		self.DONE = -100000
		self.heap = []
		self.priorities = {}  # Map from state to priority

	# Insert |state| into the heap with priority |newPriority| if
	# |state| isn't in the heap or |newPriority| is smaller than the existing
	# priority.
	# Return whether the priority queue was updated.
	def update(self, state, newPriority):
		oldPriority = self.priorities.get(state)
		if oldPriority == None or newPriority < oldPriority:
			self.priorities[state] = newPriority
			heapq.heappush(self.heap, (newPriority, state))
			return True
		return False

	# Returns (state with minimum priority, priority)
	# or (None, None) if the priority queue is empty.
	def removeMin(self):
		while len(self.heap) > 0:
			priority, state = heapq.heappop(self.heap)
			if self.priorities[state] == self.DONE: continue  # Outdated priority, skip
			self.priorities[state] = self.DONE
			return (state, priority)
		return (None, None) # Nothing left...

############################################################
# Simple examples of search problems to test your code for Problem 1.

ppp = PaperPlusPlus()
ppp.loadGloveModel()

synonymn_relevance_weight = 0.7
delta_cost_weight = 0.1

def getWordSimilarity(word1, word2):
	w1 = word1.encode("utf-8").strip()
	w2 = word2.encode("utf-8").strip()
	v1 = ppp.getWordVector(w1)
	v2 = ppp.getWordVector(w2)
	vectorDistance = ppp.computeVectorDistance(v1, v2) 
	
	deltaLength = len(w2) - len(w1)
	if deltaLength > 0:
		# deltaCost = -(1 / deltaLength)
		deltaCost = -math.sqrt(deltaLength)
	else:
		deltaCost = math.sqrt(-deltaLength)

	cost = (synonymn_relevance_weight * vectorDistance) + (delta_cost_weight * deltaCost) + 5
	# print("word1: {} word2: {} distance: {} deltaLength: {} deltaCost: {} cost: {}").format(word1, word2, vectorDistance, deltaLength, deltaCost, cost)
	if cost < 0:
		return 0
	return cost

class ShittySearch(SearchProblem):
	def __init__(self, query, costFunc):
		self.query = query
		self.costFunc = costFunc
	def startState(self):
		return (SENTENCE_BEGIN, 0)
	def isGoal(self, state):
		return state[1] == len(self.query.split(" "))
	def succAndCost(self,state):
		results = []
		sentence = list(self.query.split(" "))
		if len(sentence) <= state[1]:
			return results
		eval_word = sentence[state[1]]
		synonyms = ppp.getSynonyms(eval_word)
		for syn in list(synonyms):
			#print (state, syn, sentence[state[1]])
			results.append((syn, (syn, state[1] + 1), self.costFunc(eval_word, syn)))
		return results

def segmentWords(query):
	if len(query) == 0:
		return ''

	ucs = UniformCostSearch(verbose=0)
	ucs.solve(ShittySearch(query, getWordSimilarity))

	# BEGIN_YOUR_CODE (around 3 lines of code expected)
	segmented_words = ucs.actions
	return (" ").join(segmented_words)

inputThing = ""
while(True):
	print("")
	inputThing = raw_input("Type a phrase: ")
	print("Processing...")
	print("")
	if len(inputThing) == 0:
		break
	print segmentWords(inputThing)