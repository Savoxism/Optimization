from ortools.sat.python import cp_model

def solve(board_size):
    model = cp_model.CpModel()
    
    queens = [model.NewIntVar(0, board_size - 1, 'x%i' % i)
              for i in range(board_size)]
    
    # Constraints that all queens are in different rows
    model.AddAllDifferent(queens)
    
    # Constraints that no two queens can be on the same diagonal
    for i in range(board_size):
        diag1 = []
        diag2 = []
        for j in range(board_size):
            # Create variable array for queens(j) + j
            q1 = model.NewIntVar(0, 2 * board_size, 'diag1_%i' % i)
            diag1.append(q1)
            model.Add(q1 == queens[j] + j)
            
            # Create variable array for queens(j) - j
            q2 = model.NewIntVar(-board_size, board_size, 'diag2_%i' % i)
            diag2.append(q2)
            model.Add(q2 == queens[j] - j)
            
        model.AddAllDifferent(diag1)
        model.AddAllDifferent(diag2)
        
        solver = cp_model.CpSolver()
        solution_printer = SolutionPrinter(queens) 
        status = solver.SearchForAllSolutions(model, solution_printer)
        
        print()
        print('Solutions found: %i' % solution_printer.SolutionCount())
        
        
class SolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables    
        self.__solution_count = 0
        
    def OnSolutionCallback(self):
        self.__solution_count += 1
        for v in self.__variables:
            print('%s = %i' % (v, self.Value(v)), end = ' ')
        print()
        
    def SolutionCount(self):
        return self.__solution_count
    
def main():
    board_size = 4
    solve(board_size)
    
if __name__ == '__main__':
    main()