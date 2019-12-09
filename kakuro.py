import csp
import sys

def sum(list):
    s = 0
    for x in list:
        s += x
    return s
    
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
                    for r in range(self.n_rows):
                        neig_list = data_list[r + 2].split()
                        for c in range(self.n_columns):
                            self.neighbor = tuple(neig_list[(3+1) * c : (3+1) * c + 3])
                            #if we find a white square that is on the same
                            #row or the same column of the original variable
                            if (self.neighbor[0] == 'W') and ((i == r) ^ (j == c)):
                                neig = r * self.n_columns + c
                                #append it to the neighbors list
                                self.neighbors[var].append(neig)

        csp.CSP.__init__(self, self.variables, self.domain, self.neighbors, self.constraints)

    def constraints(self, A, a, B, b):
        #if they have the same value, then immediately return false
        if a == b:
            return False
        #find out if they are in the same line(if there difference is exactly 1)
        if abs(B - A) == 1:
            #find the line of the neighbors, with integer division
            line_no = B // self.n_columns
            #get the squares of the line from the grid
            line = self.grid[line_no]
            #we're going to traverse the line to find the desired sum
            desired_sum = -1
            for square in line:
                #if we find a black square that contains a constraint for the sum
                if square[0] == 'B' and int(square[1]) != -1:
                    #update the desired sum and break
                    desired_sum = int(square[1])
                    break
            sum = a + b
            i = line_no * self.n_columns
            for square in line:
                if square[0] == 'W' and i != A and i != B:
                    sum += int(self.domain[i][0])
                i += 1
            if sum <= desired_sum:
                return True
            else:
                return False
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
            for square in column:
                #if we find a black square that contains a constraint for the sum
                if square[0] == 'B' and int(square[2]) != -1:
                    #update the desired sum and break
                    desired_sum = int(square[2])
                    break
            #if A and B add up to the desired sum(or less), all the constraints
            #are satisfied
            # sum = a + b
            # i = column_no
            # for square in column:
            #     if square[0] == 'W' and i != A and i != B:
            #         sum += int(self.domain[i][0])
            #         i +=


            if a + b <= desired_sum or desired_sum == -1:
                return True
            else:
                return False



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please insert as second argument the file you want to solve")
        quit()
    else:
        file = open(sys.argv[1], 'r')
        data_list = file.readlines()
        kak = kakuro(data_list)
        bt_result = csp.backtracking_search(kak)
        print(bt_result)
        print(kak.nassigns)
