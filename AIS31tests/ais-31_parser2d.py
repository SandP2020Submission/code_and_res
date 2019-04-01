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
			if file[:12] == 'ais31_sigma_':		
				if file[12:] == 'eval.csv':
					print(file)
					with open(file, 'r') as results:
						csvreader = csv.reader(results,delimiter=',')
						for row in csvreader:
							if row[0] != 'Filename':
								data.append([[int(s) for s in re.findall(r'-?\d+\.?\d*', row[0].split('_')[1][:-4])], list(map(int, row[1:]))])
								
						sorted_data = sorted(data, key=operator.itemgetter(0))
						#print(sorted_data)					
						#sorted_data = [i for i in sorted_data if i[0] == 100]
						
						#print(sorted_data)
												
						last_i = []
						temp = []
						result = []
						
						for i in sorted_data:
							if last_i == []:
								temp.append(i[1])
								#print(temp)
								last_i = i[0]
							elif i[0] == last_i:
								temp.append(i[1])
							elif i[0] != last_i:
								result.append([np.array(last_i), np.array([sum(x) for x in zip(*temp)])])
								temp = []
								temp.append(i[1])
								last_i = i[0]
								
						#print(last_i)
						
						result.append([np.array(last_i),np.array([sum(x) for x in zip(*temp)])])						
						result = np.array(result)		
						
						#print(result)

						a_passed = []
						b_passed = []

						for i in result:
							#if i[0][0] != 1 and i[0][0] != 11:
							print(i)
							a_passed.append((10-min(i[1][:6]))/10)
							b_passed.append((10-min(i[1][6:]))/10)
							
						print(len(a_passed))
						print(len(b_passed))
						
						a = []
						b = []
						for i in range (0,len(a_passed),11):
							a.append(a_passed[i:i+11])
							b.append(b_passed[i:i+11])
						
						a = np.array(a)
						b = np.array(b)
						
						xax = []
						
						for i in range (0,101):
							xax.append(float(int(i)/100.00))	
						
						plt.rcParams.update({'font.size': 10})					
						
						plt.plot(xax,a_passed,label='procedureA')
						
						plt.plot(xax,b_passed,label='procedureB')
						
						plt.legend()
						
						plt.xlabel('sigma')
						plt.ylabel('probability of failure')
						
						plt.yticks(np.arange(0, 1.1, step=0.1))
						plt.grid(b=True, which='major', linestyle='-')
						
						plt.show()
						
						
if __name__ == "__main__":
	main(sys.argv[1::])
		