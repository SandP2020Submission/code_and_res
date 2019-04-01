import os, sys, getopt
import ais31tests_new as ais31
import pprint
import csv


def main(argv):
	inputfile = []
	outputfile = ''
	
	# select input dir and output file
	try:
		opts, args = getopt.getopt(argv,"hi:o",["idir=","ofile"])
	except getopt.GetoptError:
		print('test.py -i <inputdir> -o <outputfile>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print('test.py -i <inputdir> -o <outputfile>')
			sys.exit()
		elif opt in ("-i", "--idir"):
			inputdir = arg
		elif opt in ("-o", "--ofile"):
			outputfile = arg
		
	# populate a list of filenames		
	for (dirpath, dirnames, filenames) in os.walk(inputdir):		
		inputfile = filenames
	
	
		
	for file in inputfile:
		if file[-4:] == '.bin':				
			f = open(inputdir+file,'rb')
			print(file)
			b = f.read()
			stats,cnt = ais31.test7(b)
			print(stats)
	
if __name__ == "__main__":
	main(sys.argv[1::])