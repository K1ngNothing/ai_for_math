from solver import Solver
from checker import Checker
from fixer import  Fixer
from parser import ResponseParser
from logTools import LogLevel


class Coordinator:
    def __init__(self, log_level=LogLevel.RELEASE):
        self.solver = Solver(log_level)
        self.checker = Checker(log_level)
        self.fixer = Fixer(log_level)
        self.parser = ResponseParser()
        self.fixer_max_attempts = 3

    def solve(self, task):
        solution = self.solver.solve(task)
        feedback = self.checker.check(solution['solution'], solution['answer'])
        if feedback['verdict'] == 'CORRECT':
            return solution

        for _ in range(self.fixer_max_attempts):
            solution = self.fixer.fix(task, solution['solution'], feedback['issues'] + '\nVerdict is: ' + feedback['verdict'])
            feedback = self.checker.check(solution['solution'], solution['answer'])
            if feedback['verdict'] == 'CORRECT':
                return solution

        raise RuntimeError("Coordinator: Fixer exceeded maximums attempts")
