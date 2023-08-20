import numpy as np
from mpmath import *
import matplotlib.pyplot as plt
plt.style.use('dark_background')
from ApproximateEntropy import ApproximateEntropy as aet
from Complexity import ComplexityTest as ct
from CumulativeSum import CumulativeSums as cst
from FrequencyTest import FrequencyTest as ft
from Matrix import Matrix as mt
from RandomExcursions import RandomExcursions as ret
from RunTest import RunTest as rt
from Serial import Serial as serial
from Spectral import SpectralTest as st
from TemplateMatching import TemplateMatching as tm
from Universal import Universal as ut

_test_type = ['01. Frequency Test (Monobit)',
			'02. Frequency Test within a Block',
			'03. Run Test',
			'04. Longest Run of Ones in a Block',
			'05. Binary Matrix Rank Test',
			'06. Discrete Fourier Transform (Spectral) Test',
			'07. Non-Overlapping Template Matching Test',
			'08. Overlapping Template Matching Test',
			'09. Maurer\'s Universal Statistical test',
			'10. Linear Complexity Test',
			'11. Serial test (0)',
			'11. Serial test (1)',
			'12. Approximate Entropy Test',
			'13. Cummulative Sums (Forward) Test',
			'14. Cummulative Sums (Reverse) Test',
			'15. Random Excursions Test',
			'16. Random Excursions Variant Test']


__test_function = {
			0:ft.monobit_test,
			1:ft.block_frequency,
			2:rt.run_test,
			3:rt.longest_one_block_test,
			4:mt.binary_matrix_rank_text,
			5:st.spectral_test,
			6:tm.non_overlapping_test,
			7:tm.overlapping_patterns,
			8:ut.statistical_test,
			9:ct.linear_complexity_test,
			10:serial.serial_test,
			11:serial.serial_test,
			12:aet.approximate_entropy_test,
			13:cst.cumulative_sums_test,
			14:cst.cumulative_sums_test,
			15:ret.random_excursions_test,
			16:ret.variant_test
		}

def get_result_string(result):
	if result == True:
		return 'Random'
	else:
		return 'Non-Random'

def attractor(x, y, sym):
	P = [mpf('3'), mpf('3'), mpf('4'), mpf('4'), sym]
	x = (sin(P[0]*y) + P[2]*cos(P[0]* x)) * P[4]
	y = (sin(P[1]*x) + P[3]*cos(P[1]* y)) * (1 - P[4])

	return x, y

def threshhold(string):

	biString = ""

	for symb in string:
		if int(symb)%2 == 0:
			biString = biString + '0'
		else:
			biString = biString + '1'

	return biString

def draw_map(steps, start, sym):
	n = steps
	x_arr, y_arr = [], []
	arr = ""
	x_arr.append(start[0]), y_arr.append(start[1])
	for i in range(steps):
		x, y = attractor(x_arr[-1], y_arr[-1], sym)
		if x<0:
			x = -x
		if y<0:
			y = -y
		strx = str(x%1).replace("0.","")
		strx = str(y%1).replace("0.","")
		if strx.find(".") == -1 and len(strx)>10:
			arr = arr + threshhold(strx[10])     

		x_arr.append(x)
		y_arr.append(y)  

	output = open("output.txt", "w")
	output.write(arr)
	output.close()

	#print(arr)

	return x_arr, y_arr

mp.prec = 53
mp.dps = 15
symStep = mpf('0.01')
step = 0
symInterval = [mpf('-1'), mpf('0')]
sym = symInterval[0]
results = {'sym': []}
for testType in _test_type:
	results[testType] = []
	results[testType + '_testResult'] = []
while sym <= symInterval[1]:

	steps = 10000
	draw_map(steps, [mpf('-1'), mpf('-1')], sym)

	_test_result = []
	_test_string = []
	input = []
	temp = []
	handle = open("output.txt")
	for data in handle:
		temp.append(data.strip().rstrip())
	test_data = ''.join(temp)
	input.append(test_data[:1000000])
	for testData in input:
		count = 0
		res = [(), (), (), (), (), (), (), (), (), (), (), (), (), (), ()]
		for testNumber in range(15):
			try:
				if count == 14:
					res[count] = __test_function[count](test_data, mode=1)
				elif count == 10:
					res[count] = __test_function[count](test_data)[0]
				elif count == 11:
					res[count] = __test_function[count](test_data)[1]
				else:
					res[count] = __test_function[count](test_data)
				results[_test_type[count]].append(res[count][0])
				results[_test_type[count]+'_testResult'].append(res[count][1])
			except:
				results[_test_type[count]].append(0)
				results[_test_type[count]+'_testResult'].append(False)
			count += 1
		_test_result.append(res)

	results['sym'].append(sym)
	step = step + 1
	sym = sym + symStep

for testNumber in range(15):
	if testNumber == 8:
		continue
	accepted = []
	refused = []
	acceptedSym = []
	refusedSym = []
	for i in range(step):
		if results[_test_type[testNumber]+'_testResult'][i] == True:
			accepted.append(results[_test_type[testNumber]][i])
			acceptedSym.append(results['sym'][i])
		else:
			refused.append(results[_test_type[testNumber]][i])
			refusedSym.append(results['sym'][i])
	testPlotResult, testPlotAccepted, testPlotRefused = plt.plot(results['sym'], results[_test_type[testNumber]], 'b', 
	  acceptedSym, accepted, 'g^',
	  refusedSym, refused, 'ro')
	plt.title(_test_type[testNumber])
	plt.xlabel("sym")
	plt.ylabel("result")
	plt.legend(['Result','Accepted','Refused'], loc=2)
	plt.savefig("plots_myalg/"+_test_type[testNumber]+".png")
	testPlotResult.remove()
	testPlotAccepted.remove()
	testPlotRefused.remove()