import csv
import sys

def solve(tableau):

	__show(tableau)

	while not __satisfy_stop_condition(tableau):

	  	max_non_basic = __get_max_non_basic(tableau)
		min_basic, index_min_basic = __get_min_basic(tableau, max_non_basic)
		tableau = __change_base(tableau, max_non_basic, index_min_basic) # ver se ja nao atualiza sem ter que retornar.. acho que ja atualiza 

		__show(tableau)


def __show(tableau):

	def __print_formated(l):
		for e in l:
			sys.stdout.write('|{0:>7}'.format(e))
		sys.stdout.write('|\n')

	print '\n'

	__print_formated(['','LD'] + ['x'+str(x-1) for x in tableau[0]])
	__print_formated(tableau[1])

	x_asterisc = []

	for i in xrange(2, len(tableau)):
		__print_formated(['x'+str(tableau[i][0]-1)] + tableau[i][1:])
		x_asterisc.append((tableau[i][0]-2, tableau[i][1]))

	l = [0.0] * len(tableau[0])
	for e in x_asterisc: 
		l[e[0]] = e[1]

	sys.stdout.write('z* = ' + str(tableau[1][1]) + ' x* = (' + ' '.join(map(str, l)) + ')\n')

	sys.stdout.flush()

	with open('file.csv', 'a') as f:
		writer = csv.writer(f)
		writer.writerow([''] * len(tableau[1]))
		writer.writerow(['','LD'] + ['x'+str(x-1) for x in tableau[0]])
		writer.writerow(tableau[1])
		for i in xrange(2, len(tableau)):
			writer.writerow(['x'+str(tableau[i][0])] + tableau[i][1:])


def __satisfy_stop_condition(tableau):
	return max(tableau[1][1:]) <= 0

def __change_base(tableau, max_non_basic, index_min_basic):

	div = tableau[index_min_basic][max_non_basic]

	tableau[index_min_basic][1:] = [x/div for x in tableau[index_min_basic][1:]] 

	tmp = range(1, len(tableau))
	tmp.remove(index_min_basic)

	for i in tmp:
		b = -tableau[i][max_non_basic]
		tmp = [x * b for x in tableau[index_min_basic][1:]]
		tableau[i][1:] = [a + b for a, b in zip(tmp, tableau[i][1:])]

	tableau[index_min_basic][0] = max_non_basic

	return tableau


def __get_max_non_basic(tableau):

	# J non_basic
	# I basic

	I = [row[0] for row in tableau[2:]]
	J = [x for x in tableau[0] if x not in I]

	index = J[0]
	max_non_basic = tableau[1][J[0]] 

	for j in J[1:]:
		if tableau[1][j] > max_non_basic:
			index = j
			max_non_basic = tableau[1][j]

	return index


def __get_min_basic(tableau, j):

	l = []
	for i in xrange(2, len(tableau)):
		if tableau[i][j] > 0:
			l.append((tableau[i][0], tableau[i][1]/tableau[i][j], i))

	if l == []:
		print "deu ruim"
		return None

	min_basic_div = l[0]
	for div in l[1:]:
		if div[1] < min_basic_div[1]:
			min_basic_div = div

	return min_basic_div[0], min_basic_div[2]
