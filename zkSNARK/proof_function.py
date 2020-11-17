import sys

from pysnark.runtime import PrivVal, PubVal, snark
from pysnark.branching import BranchingValues, if_then_else, _if, _elif, _else, _endif, _range, _while, _endwhile, _endfor, _breakif

# from pysnark.my_runtime import snark

@snark
def tuple_compare(x, y):
    _ = BranchingValues()
    r1 = (x[0] == y[0])
    r2 = (x[1] == y[1])
    if _if(r1):
        if _if(r2):
            _.x = 0
        if _else():
            _.x = 1
        _endif()
    if _else():
        _.x = 1
    _endif()

    return _.x

@snark
def checkVotes(x, y):

	prodPuzzles = x[0]
	numVoters = x[1]
	voteFactors = y


	_ = BranchingValues()


	#check number of votes
	# r1 = (len(y) > numVoters//PubVal(2))
	r1 = (len(y) > numVoters//2)
	if _if(r1):
		_.x = 1					
	if _else():
		_.x = 0
	_endif()

	return _.x

@snark
def comparisons(x):
	print(x)
	if x.value == 1 or x.value == 0:
		return 0
	return x-1 + comparisons(x-1)

@snark
def votes(x, y):
	"""
	Function to prove that candidate got most votes

	x = [productOfPuzzles, numberOfVoters]			#public inputs
	y = [(voter1Factors), (voter2Favtors), ...]		#private inputs

	returns 0 if true, 1 if failed
	"""

	#TODO: y is currently public too because my_runtime broke the branching
	#That needs to be checked

	prodPuzzles = x[0]
	numVoters = x[1]
	voteFactors = y

	_ = BranchingValues()

	#CHECK NUMBER OF VOTES
	_.v1 = 0
	r1 = (len(y) > numVoters//2)
	if _if(r1):
		_.v1 = 1					
	_endif()


	
	#CHECK FOR DUPLICATES
	
	numComparisons = comparisons(len(y))
	val = 0
	_.v2 = 0
	_.tempVal = 0

	# #TODO: The ifs inside for are causing unreachable code, and _breakif doesn't seem to work
	# for i in _range(0, len(y)-1, max = len(y)-1):
	# 	for j in _range(i+1, len(y), max = len(y)):
	# 		print(y[i], y[j])
	# 		val = tuple_compare(y[i], y[j])
	# 		_.v2 = val
	# 		_breakif(val == 0)
	# 	val = _.v2
	# 	_breakif(val == 0)
	# print('out')

	#Inefficient code with sum instead of breaking
	for i in _range(len(y)-1, max = len(y)-1):
		for j in _range(i+1, len(y), max = len(y)):
			print(y[i], y[j])
			_.tempVal += tuple_compare(y[i], y[j])
		_endfor()
	_endfor()
	print('out')
	print(numComparisons, _.tempVal)
	
	r1 = (numComparisons == _.tempVal)

	#TODO: This is also unreachable?
	if _if(r1):
		_.v2 = 1
	if _else():
		_.v2 = 0
	_endif()



	#COMPUTE REMAINDER

	#Compute product of factors
	prod = 1
	for i in range(len(y)):
		prod *= y[i][0]*y[i][1]

	#Manually computing remainder because my_runtime broke the branching
	if prod.value==0: 
		raise ValueError("division by zero")
	quo = PrivVal(prodPuzzles.value//prod.value)
	rem = PrivVal(prodPuzzles.value-quo.value*prod.value)
	rem.assert_positive(prod.value.bit_length())

	#Check value of remainder, and set return value
	_.v3 = 0
	r1 = (rem == 0)
	if _if(r1):
		_.v3 = 1
	_endif()

	print(_.v1*_.v2*_.v3)
	return _.v1*_.v2*_.v3
	
#Divisible
x = [96, 5]
y = [(1,2),(3,4),(1,2), (2,3)]

# #Not divisible
# x = [100, 5]
# y = [(1,2),(3,4),(1,2)]

votes(x, y)