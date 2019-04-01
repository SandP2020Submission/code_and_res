import os, sys, getopt, pprint, operator
import math
import random
import csv
import re	
from collections import Counter 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy import stats, io

def main(argv):
	inputfile = []
	results = [[[] for j in range (0,11)] for i in range (0,11)]*11
	indices = []
	data = []
	
	# select input dir and output file
	try:
		opts, args = getopt.getopt(argv,"hi:o",["idir=","ofile"])
	
	except getopt.GetoptError:
		print('test.py -i <inputdir> -o <output file>')
		sys.exit(2)
	
	for opt, arg in opts:
		if opt == '-h':
			print('test.py -i <inputdir> -o <output file>')
			sys.exit()
		elif opt in ("-i", "--idir"):
			inputdir = arg
		elif opt in ("-o", "--ofile"):
			outputfile = args
			
	# populate a list of filenames		
	for (dirpath, dirnames, filenames) in os.walk(inputdir):		
		inputfile = filenames
	
	for file in inputfile:
			if file[:6] == 'ais31_':		
				if file[6:] == 'eval.csv':
					print(file)
					with open(file, 'r') as results:
						csvreader = csv.reader(results,delimiter=',')
						for row in csvreader:
							if row[0] != 'Filename':
								data.append([[int(s) for s in re.findall(r'-?\d+\.?\d*', row[0].split('_')[1][:-4])], list(map(int, row[1:]))])
								
						sorted_data = sorted(data, key=operator.itemgetter(0))
						
						last_i = []
						temp = []
						result = []
						
						for i in sorted_data:
							if last_i == []:
								temp.append(i[1])
								last_i = i[0]
							elif i[0] == last_i:
								temp.append(i[1])
							elif i[0] != last_i:
								result.append([np.array(last_i), np.array([sum(x) for x in zip(*temp)])])
								temp = []
								temp.append(i[1])
								last_i = i[0]
						
						result.append([np.array(last_i),np.array([sum(x) for x in zip(*temp)])])						
						result = np.array(result)		

						a_passed = []
						b_passed = []

						for i in result:
							if i[0][0] != 1 and i[0][0] != 11:
								a_passed.append(11-min(i[1][:6]))
								b_passed.append(11-min(i[1][6:]))
						
						a = []
						b = []
						for i in range (0,len(a_passed),11):
							a.append(a_passed[i:i+11])
							b.append(b_passed[i:i+11])
						
						a = np.array(a)
						b = np.array(b)
						
						print(a)
						
						x = []
						y = []
						for i in range (0,11):
							if i == 0:
								x.append(0)
								y.append(0)
							else:
								x.append(i/10)
								y.append(i/10)
								
						X,Y = np.meshgrid(x,y)		
						
						plt.rcParams.update({'font.size': 10})
						
						fig = plt.figure()
						ax = fig.add_subplot(111, projection='3d')
						ax.set_xlabel('es')
						ax.set_ylabel('p')
						ax.set_zlabel('Procedure A Failures')

						ax.plot_surface(X,Y,a)

						fig2 = plt.figure()
						ax2 = fig2.add_subplot(111, projection='3d')
						ax2.set_xlabel('es')
						ax2.set_ylabel('p')
						ax2.set_zlabel('Procedure B Failures')

						ax2.plot_surface(X,Y,b)
						
						plt.show()
						
						
if __name__ == "__main__":
	main(sys.argv[1::])
		