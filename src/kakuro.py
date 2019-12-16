import csp
import sys
from functions import *
import time

class kakuro(csp.CSP):
    def __init__(self, data_list):
        #create a list of lists of tuples, to keep our data
        self.grid = []
        #find out how many rows and how many columns we have in the file
        self.n_rows = int(data_list[0])
        self.n_columns = int(data_list[1])
        #keep our variables
        self.variables = []
        #keep our domain
        self.domain = {}
        #keep the neighbors
        self.neighbors = {}

        #traverse the matrix to fill the data that we need
        for i in range(self.n_rows):
            self.grid.append([])
            #get the i-th line of the matrix
            list = data_list[i + 2].split()
            for j in range(self.n_columns):
                #save each element of the matrix as a tuple that contains all
                #of its data
                square = tuple(list[(3+1) * j : (3+1) * j + 3])
                #append it to the data
                self.grid[i].append(square)
                #if it is a white square, we want to add it to our variables,
                #and find its neighbors
                if square[0] == 'W':
                    #use a linear indexing
                    var = i * self.n_columns + j
                    self.variables.append(var)
                    #update the domain of the variable with all possible values
                    self.domain[var] = [n + 1 for n in range(9)]
                    self.neighbors[var] = []
                    #find the neighbors of the variable, by traversing again
                    #our list
                    temp_horizontal = []
                    temp_vertical = []
                    for r in range(self.n_rows):
                        neig_list = data_list[r + 2].split()
                        for c in range(self.n_columns):
                            self.neighbor = tuple(neig_list[(3+1) * c : (3+1) * c + 3])
                            #if we find a white square that is on the same
                            #row or the same column of the original variable
                            if (self.neighbor[0] == 'W') and ((i == r)):
                                neig = r * self.n_columns + c
                                #append it to the neighbors list
                                temp_horizontal.append(neig)
                    #and then find the true neighbors
                    temp_horizontal = group_consecutives(var, temp_horizontal)
                    temp_vertical = []
                    for r in range(self.n_rows):
                        neig_list = data_list[r + 2].split()
                        for c in range(self.n_columns):
                            self.neighbor = tuple(neig_list[(3+1) * c : (3+1) * c + 3])
                            #if we find a white square that is on the same
                            #row or the same column of the original variable
                            if (self.neighbor[0] == 'W') and ((j == c)):
                                neig = r * self.n_columns + c
                                #append it to the neighbors list
                                temp_vertical.append(neig)
                    #and then find the true neighbors
                    temp_vertical = group_consecutives(var, temp_vertical, self.n_columns)
                    self.neighbors[var] = Union(temp_vertical,temp_horizontal)
                    self.neighbors[var].remove(var)
        csp.CSP.__init__(self, self.variables, self.domain, self.neighbors, self.constraints)

    def constraints(self, A, a, B, b):
        #if they have the same value, then immediately return false
        if a == b:
            return False
        #find out if they are in the same line(if there difference is exactly 1)
        if abs(B - A) < self.n_columns:
            #find the line of the neighbors, with integer division
            line_no = B // self.n_columns
            #get the squares of the line from the grid
            line = self.grid[line_no]
            #we're going to traverse the line to find the desired sum
            desired_sum = -1
            total_variables = 0
            ind = A % self.n_columns
            for square in line[ind::-1]:
                #if we find a black square that contains a constraint for the sum
                if square[0] == 'B' and  int(square[1]) != -1:
                    #update the desired sum and break
                    desired_sum = int(square[1])
                    break

        #if A and B are on the same column
        else:
            #find the column of the neighbors, by modulo operation
            column_no = B % self.n_columns
            #get the squares of the column from the grid
            column = []
            for line in self.grid:
                column.append(line[column_no])
            #we're going to traverse the column to find the desired sum
            desired_sum = -1
            total_variables = 0
            ind = A // self.n_rows
            for square in column[ind::-1]:
                #if we find a black square that contains a constraint for the sum
                if square[0] == 'B' and int(square[2]) != -1:
                    #update the desired sum and break
                    desired_sum = int(square[2])
                    break

        if desired_sum == -1:
            return True
        #find the other assigned values
        all_assigned = self.infer_assignment()
        sum = a + b
        completed = True
        for n in intersect(self.neighbors[A],self.neighbors[B]):
            #if we find the neighbor in the neighbors of either A or B
            if n in all_assigned:
                #increase our sum
                sum += all_assigned[n]
            #else, we havent yet completed this line / column
            else:
                completed = False
        #if the line/column is completed, return true if the sum meets the constraint
        if completed == True:
            if sum == desired_sum:
                return True
            else:
                return False
        #if not, return true if the sum is less than the constraint
        else :
            if sum < desired_sum:
                return True
            else:
                return False


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please insert as second argument the file you want to solve")
        quit()
    else:
        #open the input file given
        file = open(sys.argv[1], 'r')
        #organize its lines into a list
        data_list = file.readlines()
        print("Solving a %d x %d kakuro" % (int(data_list[0]),int(data_list[1])))
        # Solution with backtracking
        print("BT")
        #initialize the csp
        bt_kak = kakuro(data_list)
        start = time.time()
        bt_result = csp.backtracking_search(bt_kak)
        end = time.time()
        print("Time elapsed: %.5f" % (end - start))
        print("Assignments", bt_kak.nassigns)
        print("-----------------------------------")

        # Solution with backtracking
        print("BT+MRV")
        #initialize the csp
        btmrv_kak = kakuro(data_list)
        start = time.time()
        btmrv_result = csp.backtracking_search(btmrv_kak,select_unassigned_variable=csp.mrv)
        end = time.time()
        print("Time elapsed: %.5f" % (end - start))
        print("Assignments", btmrv_kak.nassigns)
        print("-----------------------------------")
        #Solution with forward checking
        print("FC")
        #initialize the csp
        fc_kak = kakuro(data_list)
        start = time.time()
        fc_result = csp.backtracking_search(fc_kak, inference = csp.forward_checking)
        end = time.time()
        print("Time elapsed: %.5f" % (end - start))
        print("Assignments", fc_kak.nassigns)
        print("-----------------------------------")

        #Solution with forward checking + mrv
        print("FC+MRV")
        #initialize the csp
        fcmrv_kak = kakuro(data_list)
        start = time.time()
        fcmrv_result = csp. backtracking_search(fcmrv_kak,select_unassigned_variable=csp.mrv,inference=csp.forward_checking)
        end = time.time()
        print("Time elapsed: %.5f" % (end - start))
        print("Assignments", fcmrv_kak.nassigns)
        print("-----------------------------------")

        #Solution with forward checking + mrv
        print("MAC")
        #initialize the csp
        mac_kak = kakuro(data_list)
        start = time.time()
        mac_result = csp.backtracking_search(mac_kak,inference=csp.mac)
        end = time.time()
        print("Time elapsed: %.5f" % (end - start))
        print("Assignments", mac_kak.nassigns)
        print("-----------------------------------")

        print("Result:", bt_result)
