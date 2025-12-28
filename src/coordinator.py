from solver import Solver
from checker import Checker
from fixer import  Fixer
from parser import ResponseParser

class Coordinator:
    def __init__(self):
        self.solver = Solver()
        self.checker = Checker()
        self.fixer = Fixer()
        self.parser = ResponseParser()
        self.max_attempts = 3
        
    def solve(self, task):
        solution = self.solver.solve(task)
        feedback = self.checker.check(solution['solution'], solution['answer'])
        if feedback['verdict'] == 'CORRECT':
            return solution['answer']
        
        curr_attempts = 0
        while curr_attempts < self.max_attempts:
            solution = self.fixer.fix(task, solution['solution'], feedback['issues'] + '\nVerdict is: ' + feedback['verdict'])
            feedback = self.checker.check(solution['corrected_solution'], solution['corrected_answer'])
            if feedback['verdict'] == 'CORRECT':
                return solution['answer']
            curr_attempts += 1

