#Based on Zhu et al's improved minimum entropy calculation for SP800-90B
import csv
import time
import struct
import math
import os, sys, getopt
from bitstring import BitArray
from collections import Counter
from statistics import mode

def improved_entropy(fn):
	w = 16

	with open (fn,'rb') as input:
		b = BitArray(input.read(125000))

		while True:
			s = []
			
			for i in range (0,len(b)-(w)):
				s.append(b[i:i+w].bin)
			B = Counter(s)
			key_min = min(B.keys(),key=(lambda k: B[k]))

			m = [[] for i in range (len(B))]
				
			if (B[key_min] < 166):
				w -= 1
			else:
				for i in range (0,len(b)-(w+1)):
					m[list(B).index(b[i:i+w].bin)].append(int(b[i+w+1]))
				break

		M = [max(Counter(x).values()) for x in m]
		p = 0
		 
		for i in M:
			p += i
			
		p = p/(len(b)-w)
			
		p_99 = min([1,p+(2.576*math.sqrt((p*(1-p))/(len(b)-w)))])

		
		min_ent = -math.log2(p_99)
		return w, p, p_99, min_ent

	input.close()