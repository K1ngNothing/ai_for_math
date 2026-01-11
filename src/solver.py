from agent import Agent
from logTools import LogLevel


class Solver(Agent):
    def __init__(self, log_level):
        super().__init__(log_level)

        self.solver_prompt = self._read_sys_prompt('prompts/solver.txt')
        self.agent_name = 'Solver'
        self.color = 'green'

    def _parse_response(self, llm_response):
        return self.response_parser.parse_solver_response(llm_response)

    def solve(self, task):
        prompt = self.solver_prompt + task
        self._log(LogLevel.RELEASE, 'Sending request to llm...')
        self._log(LogLevel.DEBUG, f'Solver prompt: {prompt}')
        response = self._send_request(prompt)
        if response['content']:
            self._log(LogLevel.DEBUG, f'Received solution from llm:\n{response}')
            self._log(LogLevel.RELEASE, 'Parsing response...')
            solution = self._parse_response(response['content'])
            self._log(LogLevel.DEBUG, f'Extracted solution is:\n{solution['solution']}')
            self._log(LogLevel.RELEASE, f'Extracted answer is: {solution['answer']}')
            return solution
        else:
            raise RuntimeError(f'error during solving task {response['error']}')
