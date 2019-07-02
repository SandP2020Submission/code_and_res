from numpy import *
from operator import add
import numpy as np
import pylab as py
import struct
import math 
from scipy.stats import linregress,chisquare,chi2,multinomial
import scipy.special as spc
from bitstring import BitArray
import pandas as pd
from itertools import islice, combinations
import collections
import met
import sys
from io import StringIO
from decimal import Decimal
from multiprocessing import Process


def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()

def window(seq, n=2):
    "Sliding window width n from seq.  From old itertools recipes."""
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

# fips140-1 test using original parameters (use rngtest utility for fips140-2)
def fips1401(f,r):
	res = []
	t1r = []
	t2r = []
	t3r = []
	t4r = []
	
	for i in range (0,r):
		x = (i*2500)
		s = f[x:x+2500]
		t1r.append(test1(s))
		t2r.append(test2(s))
		t3r.append(test3(s))
		t4r.append(test4(s))
		
		res.append(t1r)
		res.append(t2r)
		res.append(t3r)
		res.append(t4r)
		
	eval = evalFIPS(t1r,t2r,t3r,t4r)	
	
	return eval,res
	
def evalFIPS(b,c,d,e):
	eval = [0]*4
	
	for x in b:
		if(x<9654 or x>10346):
			#print(x)
			eval[0] += 1
			
	for x in c:
		if(x < 1.03 or x > 57.4):
			#print(x)
			eval[1] += 1
			
	for x in d:
		if (x[0] < 2267 or x[0] > 2733):
			#print(x)
			eval[2] += 1
		elif (x[1] < 1079 or x[1] > 1421):
			#print(x)
			eval[2] += 1
		elif (x[2] < 502 or x[2] > 748):
			#print(x)
			eval[2] += 1
		elif (x[3] < 223 or x[3] > 402):
			#print(x)
			eval[2] += 1
		elif (x[4] < 90 or x[4] > 223):
			#print(x)
			eval[2] += 1
		elif (x[5] < 90 or x[5] > 223):
			#print(x)
			eval[2] += 1
			
	for x in e:
		if(x[0] > 34 or x[1] > 34):
			#print(x)
			eval[3] += 1
			
	return eval
	
#ais31 procedure a
def procA(f):
	eval = []
	res = []
	t0r = 0
	t1r = []
	t2r = []
	t3r = []
	t4r = []
	t5r = []
	
	t0r = test0(f[0:393216])
	
	for i in range (0,257):
		x = 393216+(i*2500)
		s = f[x:x+2500]
		t1r.append(test1(s))
		t2r.append(test2(s))
		t3r.append(test3(s))
		t4r.append(test4(s))
		#t5r.append(test5(s))
		
		res.append(t0r)
		res.append(t1r)
		res.append(t2r)
		res.append(t3r)
		res.append(t4r)
		res.append(t5r)
	
	eval = evalA(t0r,t1r,t2r,t3r,t4r,t5r)	
	
	return eval,res
	
#procedure A evaluation criteria
def evalA(a,b,c,d,e,f):
	eval = [True]*6
	
	if (a>0):
		eval[0] = False
		
	for x in b:
		if(x<9654 or x>10346):
			eval[1] = False
			break
			
	for x in c:
		if(x < 1.03 or x > 57.4):
			eval[2] = False
			break
			
	for x in d:
		if (x[0] < 2267 or x[0] > 2733):
			eval[3] = False
			break
		elif (x[1] < 1079 or x[1] > 1421):
			eval[3] = False
			break
		elif (x[2] < 502 or x[2] > 748):
			eval[3] = False
			break
		elif (x[3] < 223 or x[3] > 402):
			eval[3] = False
			break
		elif (x[4] < 90 or x[4] > 223):
			eval[3] = False
			break
		elif (x[5] < 90 or x[5] > 223):
			eval[3] = False
			break
			
	for x in e:
		if(x[0] > 34 or x[1] > 34):
			eval[4] = False
			break

	for x in f:
		if(x<2326 or x>2674):
			eval[5] = False
			break
	
	return eval
	
#ais31 procedure b	
def procB(f):
		res = []
		eval = []
			
		stats = test6a(f[:12500])		
		res.append(stats)
		stats, count = test7(f[12500:])
		res.append([x for x in stats])
		stats = test8(f[12500+count:])
		res.append(stats)
		
		eval = evalB(res)
		
		return eval,res
		
def evalB(r):
	eval = [True]*9
	maxchi = chi2.isf(q=0.0001, df=1)
	
	if (r[0] > 75000 or r[0] < 25000):
		eval[0] = False
	
	for x in range (0,len(r[1])):
		if (r[1][x] > maxchi):
			eval[x+1] = False
			break
			
	if(r[2] < 7.976):
		eval[8] = False
	
	return eval

# disjointedness test (return True if pass, False if fail)
def test0(s):
	a=[]
	c = 0
	for i in range(1,65536,6):
		a.append(s[i:i+6])
			
	a=sorted(a)
	
	for i in range(0,len(a)-1):
		if(a[i]==a[i+1]):
			c += 1
	
	return c

#monobits test as defined in FIPS140-1
def test1(s):
	b = BitArray(s)
	c = b.count(True)
	return c
	
#poker test as defined in FIPS140-1
def test2(s):
	res = [0]*16
	h = ''.join(format(x, '02x') for x in s)
	for i in h:
		res[int(i,16)] = res[int(i,16)]+1
		
	sres = [x**2 for x in res]
	tres = sum(sres)
	fres = (16 / 5000)*tres-5000
	
	return fres
	
#runs test as defined in FIPS140-1
def test3(s):
	b = BitArray(s)
	c = [0] * 6
	cnt = 0
	
	for i in range (0,len(b)-1):
		if (b[i]==b[i+1]):
			cnt = cnt+1			
		else:
			if (cnt < 6 and cnt > 0):
				c[cnt-1] = c[cnt-1]+1
			elif(cnt >= 6):
				c[5] = c[5] + 1
			cnt = 0	
	return c

#long run test as defined in FIPS140-1	- self evaluates
def test4(s):
	res = True
	b = BitArray(s)
	c = [0,0]
	
	for i in b:
		if (i is False):
			c[1] = 0
			c[0] = c0+1
			if(c0>34):
				break;
		elif (i is True):
			c[0] = 0
			c[1] = c1+1
			if(c1>34):
				break;
	
	return c

#auto-correlation test
def test5(s):		
	t = []
	b = BitArray(s)
	
	
	for i in range(1,5001):
		for j in range(1,5001):
			temp = b[j]^b[j+i]
		t.append(temp)
	
	return sum(t)

#uniform distribution test (multinomial test variant)
def test6a(s):
	b = BitArray(s)
	c=0
	L = 100000
	
	for i in range (0,L):
		if (b[i]==1):
			c=c+1
		
	return c

#homogeneity test variants (6b, 7a, and 7b)
def test7(s):
	res = True
	b = BitArray(s)
	w2 = [[] for i in range (2)]
	w3 = [[] for i in range (4)]
	w4 = [[] for i in range (8)]
	vemp = []	
	stats = []
	a = 0 #significance level (set depending on test number)
	t = 0
	n = 100000
	cnt = 0
	max_chi = 0
	
	for k in [2,3,4]:
		f = 0
		b = b[cnt:]
		for i in range (cnt,len(b),k):
			temp = b[i:i+k]
			
			if (k==2):
				if (temp[0] == False):
					w2[0].append(temp)
				elif (temp[0] == True):
					w2[1].append(temp)
					
				if (min([len(x) for x in w2])>=n):
					break
				elif (max([len(x) for x in w2]) >= 10*n and min([len(x) for x in w2]) == 0):
					print("Deadman counter exceeded, test failed.")
					return stats,res,int(cnt/8)
				
					
			if (k==3):
				if (temp[0] == False and temp[1] == False):
					w3[0].append(temp)
				elif (temp[0] == True and temp[1] == False):
					w3[1].append(temp)
				elif (temp[0] == False and temp[1] == True):
					w3[2].append(temp)
				elif (temp[0] == True and temp[1] == True):
					w3[3].append(temp)
					
				if (min([len(x) for x in w3])>=n):
					break
				elif (max([len(x) for x in w3]) >= 10*n and min([len(x) for x in w3]) == 0):
					print("Deadman counter exceeded, test failed.")
					return stats,res,int(cnt/8)
				
			
			if (k==4):
				if (temp[0] == False and temp[1] == False and temp[2] == False):
					w4[0].append(temp)
				elif (temp[0] == True and temp[1] == False and temp[2] == False):
					w4[1].append(temp)
				elif (temp[0] == False and temp[1] == True and temp[2] == False):
					w4[2].append(temp)
				elif (temp[0] == True and temp[1] == True and temp[2] == False):
					w4[3].append(temp)
				elif (temp[0] == False and temp[1] == False and temp[2] == True):
					w4[4].append(temp)
				elif (temp[0] == True and temp[1] == False and temp[2] == True):
					w4[5].append(temp)
				elif (temp[0] == False and temp[1] == True and temp[2] == True):
					w4[6].append(temp)
				elif (temp[0] == True and temp[1] == True and temp[2] == True):
					w4[7].append(temp)
			
				if (min([len(x) for x in w4])>=n):
					break
				elif (max([len(x) for x in w4]) >= 10*n and min([len(x) for x in w4]) == 0):
					print("Deadman counter exceeded, test failed.")
					return stats,int(cnt/8)
				
			cnt += k
		
		if (k==2):
			tmp = []
			probs = []
				
			for i in range (len(w2)):
				tmp.append([str(j) for j in w2[i]])	
			
			for i in range (len(tmp)):
				freq, M = transmat(tmp[i][:n])
				probs.append(M)
				
			tprobs = pd.concat(probs)
			#print(tprobs)
				
			stats.append(float(probs[0]['1'])+float(probs[1]['0'])-1)
		
		if (k==3):
			tmp = []
			freq = []
			probs = []
			
			for i in range (len(w3)):
				tmp.append([str(j) for j in w3[i]])
				
			for i in range (len(tmp)):
				f, M = transmat([str(j) for j in w3[i][:n]])
				freq.append(f)
				probs.append(M)
			
			#probs = np.dot(probs,probs).shape
			probs = pd.concat(probs)
			#print(probs.pow(2))
			
			T = [0]*2
			
			T[0] = T7([freq[0],freq[1]],n)
			T[1] = T7([freq[2],freq[3]],n)
			
			for i in T:
				stats.append(i)	
			
		if (k==4):
			tmp = []
			freq = []
			probs = []
			
			for i in range (len(w4)):
				tmp.append([str(j.bin) for j in w4[i]])
			
			for i in range (len(tmp)):
				f, M = transmat([str(j.bin) for j in w4[i][:n]])
				freq.append(f)
				probs.append(M)
			
			probs = pd.concat(probs)
			#print(probs.pow(3))
			
			T = [0]*4
			
			T[0] = T7([freq[0],freq[4]],n)
			T[1] = T7([freq[1],freq[5]],n)
			T[2] = T7([freq[2],freq[6]],n)
			T[3] = T7([freq[3],freq[7]],n)
			
			for i in T:
				stats.append(i)				
		
	return stats,int(cnt/8)
	
def transmat(a):			
	matrix = pd.Series(collections.Counter(map(tuple, a))).unstack().fillna(0)		
	return matrix, (matrix.divide(matrix.sum(axis=1),axis=0))
	
def T7(f,n):
	a = 0.0001
	p = [0,0]
		
	# calculate probabilities for vemp
	for i in range (len(p)):
		f_i = 0
		for j in f:
			f_i += j.iloc[0,i]
		p[i] = f_i/(2*n)
		
	#print(p)
	
	T = 0
	for i in f:
		for t in range (len(p)):
			T += (i.iloc[0,t]-(n*p[t]))**2/(n*p[t])

	return T
		
# Jean Sebastien Coron's entropy estimation test
#Code adapted from page 10 of http://www.crypto-uni.lu/jscoron/publications/entropy.pdf 
def test8(s):
		
	stats = []
	res = []
	Q = 2560
	K = 256000
	L = 8
	
	V = (1 << L)
	tab = [0]*V
	k = 0
	sum = 0
	
	for n in range (1,Q+1):
		tab[int(s[n])] = n
				
	for n in range(Q+1,Q+K+1):
		k = s[n]
		sum += fcoef(n-tab[k])
		#print(n-tab[k])
		tab[k] = n
			
	fn = sum/K
	
	#print(fn)
	
	return fn
		

def fcoef(i):
	l = log(2)
	s = 0
	C = -0.8327462
	j = i-1
	limit = 23
	
	if(i<limit):
		for k in range (1,i):
			s += (1/k)
		return s/l
	else:	
		return log(j)/l-C+(1/(2*j)-1/(12*(j**2)))/l

#shannon entropy calculation
# def ent(data):
	# Q = 2560
	# K = 256000
	# entropy = 0
	# byte_counts = [0]*256
	
	# for i in data[:Q+K]:
		# byte_counts[i] += 1
	
	# for count in byte_counts:
		# # If no bytes of this value were seen in the value, it doesn't affect
		# # the entropy of the file.

		# if (count == 0):
			# continue
		# # p is the probability of seeing this byte in the file, as a floating-
		# # point number
		# p = 1.0 * count / len(data[:Q+K])
		# entropy -= p * math.log(p, 256)
		
	# print(entropy*8)
		
	# return entropy