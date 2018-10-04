import math

def distance(A, B):
	return math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)

def distance_optimized(A, B):
	return (A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2