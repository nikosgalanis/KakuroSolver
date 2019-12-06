# from csp import *
#
# class kakuro(csp.problem):
#     def  __init__(self, n_rows, n_columns, )
import sys

class kakuro():
    def __init__(self, data_list):
        #create a list of lists of tuples, to keep our data
        self.grid = []
        #find out how many rows and how many columns we have in the file
        n_rows = int(data_list[0])
        n_columns = int(data_list[1])
        #keep our variables
        variables = []
        #keep our domain
        domain = {}
        #keep the neighbors
        neighbors = {}
        #traverse the matrix to fill the data that we need
        for i in range(n_rows):
            self.grid.append([])
            #get the i-th line of the matrix
            list = data_list[i + 2].split()
            for j in range(n_columns):
                #save each element of the matrix as a tuple that contains all
                #of its data
                square = tuple(list[(2+1) * j : (2+1) * j + 2])
                #append it to the data
                self.grid[i].append(square)
                #if it is a white square, we want to add it to our variables,
                #and find its neighbors
                if square[0] == 'W':
                    #use a linear indexing
                    var = i * n_columns + j
                    variables.append(var)
                    #update the domain of the variable with all possible values
                    domain[var] = [n + 1 for n in range(9)]
                    neighbors[var] = []
                    #find the neighbors of the variable, by traversing again
                    #our list
                    for r in range(n_rows):
                        neig_list = data_list[r + 2].split()
                        for c in range(n_columns):
                            neighbor = tuple(neig_list[(2+1) * c : (2+1) * c + 2])
                            #if we find a white square that is on the same
                            #row or the same column of the original variable
                            if (neighbor[0] == 'W') and ((i == r) ^ (j == c)):
                                neig = r * n_columns + c
                                #append it to the neighbors list
                                neighbors[var].append(neig)

        print(neighbors)
        print(self.grid)

    def constraints(self, A, a, B, b):


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please insert as second argument the file you want to solve")
        quit()
    else:
        file = open(sys.argv[1], 'r')
        data_list = file.readlines()
        kakuro(data_list)
