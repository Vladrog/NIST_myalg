import numpy as np
import matplotlib.pyplot as plt
from math import copysign, fabs, floor, isfinite, modf
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

def attractor(x, y, k, sym):
	t = x
	x = -y + sym * (abs(x)+k)
	y = t - (1 - sym)*(abs(x)+k)
	return x, y

def float_to_bin_fixed(f):
    if not isfinite(f):
        return repr(f)  # inf nan

    sign = '-' * (copysign(1.0, f) < 0)
    frac, fint = modf(fabs(f))  # split on fractional, integer parts
    n, d = frac.as_integer_ratio()  # frac = numerator / denominator
    assert d & (d - 1) == 0  # power of two
    return f'{sign}{floor(fint):b}.{n:0{d.bit_length()-1}b}'

def draw_map(steps, startPoint, k, sym): # формирование выборки для тестов 
	n = steps
	x_arr, y_arr = [], []
	arr = ""
	x_arr.append(startPoint[0]), y_arr.append(startPoint[1])
	for i in range(steps):
		x, y = attractor(x_arr[-1], y_arr[-1], k, sym) # получаем значения генератора
		if x<0:
			x = -x
		if y<0:
			y = -y   

		strx = float_to_bin_fixed(x) # перевод в двоичный вид
		stry = float_to_bin_fixed(y)
		arr = arr + strx[-5] # берем 5-ый символ с конца в бинарной строке
		x_arr.append(x)
		y_arr.append(y)  

	output = open("output.txt", "w")
	output.write(arr)
	output.close()

	#print(arr)

	return x_arr, y_arr

startPoint = [1.3, 0.1] # начальная точка
k = 1
symStep = 0.01 # шаг симметрии
step = 0
symInterval = [0.01, 1] # интервал симметрии
sym = symInterval[0]
results = {'sym': []}
for testType in _test_type:
	results[testType] = []
	results[testType + '_testResult'] = []

while sym <= symInterval[1]: # формирование выборок по sym коэф. и прохождение тестов

	steps = 10000 # количество итераций генератора
	draw_map(steps, startPoint, k, sym) # формирование выборки с текущим коэф. симметрии

	# Прохождение тестов
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

for testNumber in range(15): # рисование графиков
	if testNumber == 8:
		continue
	accepted = []
	refused = []
	acceptedSym = []
	refusedSym = []
	resultsNew = []
	for i in range(step):
		if results[_test_type[testNumber]+'_testResult'][i] == True:
			#accepted.append(results[_test_type[testNumber]][i])
			accepted.append(1)
			resultsNew.append(1)
			acceptedSym.append(results['sym'][i])
		else:
			#refused.append(results[_test_type[testNumber]][i])
			refused.append(0)
			resultsNew.append(0)
			refusedSym.append(results['sym'][i])
	testPlotResult, testPlotAccepted, testPlotRefused = plt.plot(results['sym'], resultsNew, #results[_test_type[testNumber]], 
		'b', 
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