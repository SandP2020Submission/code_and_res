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
	
	# for every file in filenames, check whether the booltest is passed or failed 	
	with open('ais31_t100_eval.csv','w') as csvfile:
		csvwriter = csv.writer(csvfile,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
		csvwriter.writerow(['Filename', 'T0', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6a', 'T6b', 'T7a_1', 'T7a_2', 'T7b_1', 'T7b_2', 'T7b_3', 'T7b_4', 'T8'])		
		
		with open('ais31_t100_statsA.csv','w') as csvstatsA:
					statswriterA = csv.writer(csvstatsA,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
					statswriterA.writerow(['Filename', 'T0', 'T1', 'T2', 'T3', 'T4', 'T5'])
					
					with open('ais31_t100_statsB.csv','w') as csvstatsB:
						statswriterB = csv.writer(csvstatsB,delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
						statswriterB.writerow(['Filename', 'T6a', 'T6b, T7a, T7b', 'T8'])
		
						for file in inputfile:
							print(file)
							if file[-4:] == '.bin':				
								f = open(inputdir+file,'rb')
								
								a = f.read(1038216)
								b = f.read(8000000)
								
								f.close()
								
								evalA, resA = ais31.procA(a)
								evalB, resB = ais31.procB(b)
				
				
								for x in range (len(resA[1])):
									statswriterA.writerow([file, resA[0], resA[1][x], resA[2][x], resA[3][x], resA[4][x], resA[5]])
									
				
								statswriterB.writerow([file, resB[0], resB[1], resB[2]])									
								csvwriter.writerow([file, int(evalA[0]), int(evalA[1]), int(evalA[2]), int(evalA[3]), int(evalA[4]), int(evalA[5]), int(evalB[0]), int(evalB[1]), int(evalB[2]), int(evalB[3]), int(evalB[4]), int(evalB[5]), int(evalB[6]), int(evalB[7]), int(evalB[8])])
	
if __name__ == "__main__":
	main(sys.argv[1::])