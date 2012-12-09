import random
from sys import argv
from mpi4py import MPI
from subset import Subset
from collections import Counter
import numpy as np

import dtree

p_root = 0
data_features_file = 'data/features.txt'
data_training_file = 'data/training/medium.txt'
data_testing_file = 'data/testing/medium.txt'
number_of_trees = 12

def print_tree(tree, str):
    """
    This function recursively crawls through the d-tree and prints it out in a
    more readable format than a straight print of the Python dict object. 
    """
    if type(tree) == dict:
        print "%s%s" % (str, tree.keys()[0])
        for item in tree.values()[0].keys():
            print "%s\t%s" % (str, item)
            print_tree(tree.values()[0][item], str + "\t")
    else:
        print "%s\t->\t%s" % (str, tree)

def parallel_create_random_forest(comm, rank, data, features):
	size = comm.Get_size()

	features = comm.bcast(features, root=p_root)
	data = comm.bcast(data, root=p_root)	

	num_trees = int(number_of_trees/size)
	if rank < number_of_trees%size:
		num_trees += 1	

	trees = []
	for t in range(num_trees):
		#boostrap sampling
		n, f = data.shape
		indices = [random.randint(0,n-1) for i in range(n)]
		subset = Subset(indices, data=data)
		decision_tree = dtree.create(subset, features)
		trees.append(decision_tree)

	forest = comm.gather(trees, root=p_root)

	if rank == p_root:
		#flatten array
		forest = [tree for trees in forest for tree in trees]

	return forest

def get_reviews():
	features = get_features()
	reviews = []

	f = open(data_testing_file, 'r+')
	for line in f:
		reviews.append(dict(zip(features, np.float64(line.split(',')))))
	f.close()

	return reviews


def get_features():
	features = []
	
	f = open(data_features_file, 'r+')
	for line in f:
		features.append(line.strip())
	f.close()

	return features

def get_data():
	data = np.loadtxt(fname=data_training_file, delimiter=',')
	return data


if __name__ == '__main__':

	comm = MPI.COMM_WORLD
	rank = comm.Get_rank()

	if rank == p_root:
		data = get_data()
		features = get_features()
	else:
		data, features = None, None

	forest = parallel_create_random_forest(comm, rank, data, features)

	if rank == p_root:
		print "Random Forest was built. Beginning classification."
		errors = 0
		reviews = get_reviews()
		for review in reviews:
			answers = []
			for tree in forest:
				answers.append(dtree.classify(tree, review))
			#print answers
			answer = Counter(answers).most_common(1)[0][0]
			if answer != review['star']:
				print "Answer: %f, Star: %f" %(answer, float(review['star'])) 
				errors += 1

		print "%i error(s) / %i reviews. %f %% accuracy" % (errors, len(reviews), float(len(reviews)-errors)/len(reviews))
