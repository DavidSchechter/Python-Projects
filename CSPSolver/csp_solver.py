__author__ = 'DavidSchechter'

# Student: David Schechter
# Student ID: 009987848
# Student: Gabe Guevara
# Student ID: 007617766

import sys
import re

#Class definition of csp_solver - a solving class for CSP problems
#x-list - a csp variable list
#d-list - a dictionary of domain list for each variable in x-list
#c-list -  a dictionary a constraint functions for a tuple of (v1,v2) were v1 and v2 are in x-list
#forward_checking_flag - to run or not run forward checking
#assignment - gets an initial assignment

class csp_solver:
	def __init__(self, temp_x_list, temp_d_list, temp_c_list, temp_x_neighbours_list, temp_forward_checking_flag,
				 temp_assignment):
		self.x_list = temp_x_list
		self.d_list = temp_d_list
		self.c_list = temp_c_list
		self.x_neighbours_list = temp_x_neighbours_list
		self.forward_checking_flag = temp_forward_checking_flag
		self.assignment = temp_assignment
		self.timesDidBackTrack = 0

	#class function for checking in var x with val a satisfies var y with val b
	#class function receives var x,val a,var y,val b
	#return true if satisfies, else false

	def constraints_evaluation(self, temp_x, a, temp_y, b):
		test_function = self.c_list[(temp_x, temp_y)]
		return test_function(a, b)

	#class function finding the the variable with minimum remaining values
	#class function implementation of MRV heuristic
	#returns a list of variable that have the minimum remaining values

	def mrv(self):
		result = []
		max_len = 0
		for p in xrange(len(self.x_list)):
			if not self.x_list[p] in self.assignment:
				temp_count = len(self.d_list[self.x_list[p]])
				if temp_count > max_len:
					max_len = temp_count
					result = [self.x_list[p]]
				elif temp_count == max_len:
					result.append(self.x_list[p])
		return result

	#class function finding the the variable that is involved in the largest number of constraints
	#class function implementation of Degree heuristic
	#returns a list of variable that are involved in the largest number of constraints

	def degree(self):
		result = []
		max_len = 0
		for w in xrange(len(self.x_list)):
			if not self.x_list[w] in self.assignment:
				temp_x_neighbours_list = self.x_neighbours_list[self.x_list[w]]
				temp_count = 0
				for q in xrange(len(temp_x_neighbours_list)):
					if not temp_x_neighbours_list[q] in self.assignment:
						temp_count += 1
				if temp_count > max_len:
					max_len = temp_count
					result = [self.x_list[w]]
				elif temp_count == max_len:
					result.append(self.x_list[w])
		return result

	#class function ordering a domain of var x by least-constraining-value heuristic
	#class function receives a var x and a domain x_domain_list
	#returns a sorted domain list by least-constraining-value

	def lcv(self, temp_x, x_domain_list):
		result = sorted(x_domain_list, key=lambda val: self.lcv_for_one_val(temp_x, val))
		return result

	#class function finding the the variable value that rules out the fewest choices for the
	# neighboring variables in the constraint graph
	#class function implementation of least-constraining-value heuristic
	#class function receives var x and val val
	#return the number of choices the val rules out for var x's neighbours

	def lcv_for_one_val(self, temp_x, val):
		num_of_removal = 0
		temp_x_neighbours_list = self.x_neighbours_list[temp_x]
		for z in xrange(len(temp_x_neighbours_list)):
			if val in self.d_list[temp_x_neighbours_list[z]]:
				num_of_removal += 1
		return num_of_removal

	#class function for checking if a var with val val is consistent with the current assignment
	#class function receives var x and val val
	#return if true returns true, else false

	def consistent_with_assignment(self, var, val):
		all_are_true = True
		for var2 in self.assignment:
			if var2 in self.x_neighbours_list[var]:
				if not self.constraints_evaluation(var, val, var2, self.assignment[var2]):
					all_are_true = False
		return all_are_true

	#class function implementation of Forward Checking
	#class function receives var x and val val and list of values_to_remove
	#returns true is arc consistency is maintained, else false

	def forward_checking(self, var, val, values_to_remove):
		if not self.forward_checking_flag:
			return True
		else:
			for var2 in self.x_neighbours_list[var]:
				if not var2 in self.assignment:
					for val2 in self.d_list[var2]:
						if not self.constraints_evaluation(var, val, var2, val2):
							# remove val2 from var2 domain
							self.d_list[var2].pop(self.d_list[var2].index(val2))
							values_to_remove.append((var2, val2))
					if len(self.d_list[var2]) == 0:
						return False
			return True

	#class function implementation of Backtrack Algorithm
	#returns a solution to csp problem is exists, else returns no solution

	def backtrack(self):
		self.timesDidBackTrack += 1
		if len(self.assignment) == len(self.x_list):
			return self.assignment
		vars_to_try = self.mrv()
		if len(vars_to_try) > 1:
			vars_to_try = self.degree()
		var_to_try = vars_to_try[0]
		temp_domain = self.d_list[var_to_try]
		temp_domain = self.lcv(var_to_try, temp_domain)
		for val in temp_domain:
			if self.consistent_with_assignment(var_to_try, val):
				# print("try to assign "+var_to_try+" with val "+str(val))
				self.assignment.update({var_to_try: val})
				values_to_remove = [(var_to_try, a) for a in self.d_list[var_to_try] if a != val]
				self.d_list[var_to_try] = [val]
				if self.forward_checking(var_to_try, val, values_to_remove):
					result = self.backtrack()
					if not result is None:
						return result
				for var_to_restore, val_to_restore in values_to_remove:
					self.d_list[var_to_restore].append(val_to_restore)
		if var_to_try in self.assignment:
			del self.assignment[var_to_try]
		return None

	#class function implementation of Backtrack Algorithm
	#returns a solution to csp problem is exists, else returns no solution

	def backtracking_search(self):
		very_temp_assignment = self.backtrack()
		return very_temp_assignment

#main function
#program expects two vars- problem_filename and use_forward_check_flag, if no returns error
#program readfile and checks that all vars and val are legal, if not returns error
#program convert file to a csp problem and run backtrack algorithm to try and solve it.
#program prints out the backtrack algorithm solution

if (len(sys.argv)) != 3:
	print "Please supply a problem_filename use_forward_check_flag to use"
	raise SystemExit(1)
else:
	filename = sys.argv[1]
	forwardCheckingFlag = sys.argv[2]
	f = open(filename)
	line = f.readline()
	# the number D of distinct variables in the file in the number of elements in x_list
	x_list = []
	d_list = {}
	c_list = {}
	unary_constraints = []
	temp_assignment = {}
	x_neighbours_list = {}
	#the largest value V of an integer in a constraint will be save by largest_v
	largest_v = 0
	while line:
		params = line.split()
		if len(params) == 3:
			if params[0][0].isalpha() and re.match("^[A-Za-z0-9_]*$", params[0]):
				if params[1] == "eq" or params[1] == "ne" or params[1] == "lt" or params[1] == "gt":
					if (params[2][0].isalpha() and re.match("^[A-Za-z0-9_]*$", params[2])) or (params[2].isdigit()):
						if not (params[0] in x_list):
							x_list.append(params[0])
							x_neighbours_list.update({params[0]: []})
							if params[2].isdigit():
								if largest_v < int(params[2]):
									largest_v = int(params[2])
							else:
								if not (params[2] in x_list):
									x_list.append(params[2])
									x_neighbours_list.update({params[2]: [params[0]]})
									if not params[2] in x_neighbours_list[params[0]]:
										x_neighbours_list[params[0]].append(params[2])
								else:
									if not params[0] in x_neighbours_list[params[2]]:
										x_neighbours_list[params[2]].append(params[0])
									if not params[2] in x_neighbours_list[params[0]]:
										x_neighbours_list[params[0]].append(params[2])
						else:
							if params[2].isdigit():
								if largest_v < int(params[2]):
									largest_v = int(params[2])
							else:
								if not (params[2] in x_list):
									x_list.append(params[2])
									x_neighbours_list.update({params[2]: [params[0]]})
									if not params[2] in x_neighbours_list[params[0]]:
										x_neighbours_list[params[0]].append(params[2])
								else:
									if not params[0] in x_neighbours_list[params[2]]:
										x_neighbours_list[params[2]].append(params[0])
									if not params[2] in x_neighbours_list[params[0]]:
										x_neighbours_list[params[0]].append(params[2])
						if params[1] == "eq":
							constraint = params[0] + " = " + params[2]
							if not params[2].isdigit():
								c_list.update({(params[0], params[2]): lambda tmp_x, y: tmp_x == y})
							else:
								unary_constraints.append(constraint)
						elif params[1] == "ne":
							constraint = params[0] + " != " + params[2]
							if not params[2].isdigit():
								c_list.update({(params[0], params[2]): lambda tmp_x, y: tmp_x != y})
							else:
								unary_constraints.append(constraint)
						elif params[1] == "lt":
							constraint = params[0] + " < " + params[2]
							if not params[2].isdigit():
								c_list.update({(params[0], params[2]): lambda tmp_x, y: tmp_x < y})
							else:
								unary_constraints.append(constraint)
						else:
							constraint = params[0] + " > " + params[2]
							if not params[2].isdigit():
								c_list.update({(params[0], params[2]): lambda tmp_x, y: tmp_x > y})
							else:
								unary_constraints.append(constraint)
					else:
						print "not a valid file"
						raise SystemExit(1)
				else:
					print "not a valid file"
					raise SystemExit(1)
			else:
				print "not a valid file"
				raise SystemExit(1)
		else:
			print "not a valid file"
			raise SystemExit(1)
		line = f.readline()
	domain = []
	domain_length = max(largest_v, len(x_list))
	for j in xrange(domain_length):
		domain.append(j)
	for i in xrange(len(x_list)):
		d_list.update({x_list[i]: domain})
	for k in xrange(len(unary_constraints)):
		temp_vars = unary_constraints[k].split()
		variable = temp_vars[0]
		constraint = temp_vars[1]
		number = int(temp_vars[2])
		var_domain = []
		if constraint == "=":
			var_domain = [x for x in domain if x == number]
			d_list[variable] = var_domain
			temp_assignment.update({variable: var_domain[0]})
		elif constraint == "!=":
			var_domain = [x for x in domain if x != number]
			d_list[variable] = var_domain
		elif constraint == "<":
			var_domain = [x for x in domain if x < number]
			d_list[variable] = var_domain
		elif constraint == ">":
			var_domain = [x for x in domain if x > number]
			d_list[variable] = var_domain
	if forwardCheckingFlag == "0":
		forwardChecking = False
	else:
		forwardChecking = True
	csp = csp_solver(x_list, d_list, c_list, x_neighbours_list, forwardChecking, temp_assignment)
	temp_assignment = csp.backtracking_search()
	if temp_assignment:
		for key in sorted(temp_assignment):
			print (key + "=" + str(temp_assignment[key]))
	else:
		print ("No Solution")
	int_check = 1