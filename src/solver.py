from agent import Agent


class Solver(Agent):
    def __init__(self):
        super().__init__()
        
        self.solver_prompt = self._read_sys_prompt('prompts/solver.txt')
        self.agent_name = 'Solver'
        self.color = 'green'
        
    def _parse_response(self, llm_response):
        return self.response_parser.parse_solver_response(llm_response)
        
    def solve(self, task):
        prompt = self.solver_prompt + task
        self._log(f'sending respone to llm with prompt: {prompt}')
        response = self._send_request(prompt)
        if response['content']:
            self._log(f'Recived solution from llm:\n{response}')
            solution = self._parse_response(response['content'])
            self._log(f'Extracted solution is:\n{solution['solution']}')
            self._log(f'Extracted answer is:\n{solution['answer']}')
            return solution
        else:
            raise RuntimeError(f'error during solving task {response['error']}')
    