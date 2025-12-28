from agent import Agent


class Fixer(Agent):
    def __init__(self):
        super().__init__()

        self.fixer_prompt = self._read_sys_prompt('prompts/fixer.txt')
        self.agent_name = 'Fixer'
        self.color = 'blue'
        
    def _parse_response(self, llm_response):
        return self.response_parser.parse_fixer_response(llm_response)
        
    def _make_fixer_prompt(self, task, solution, feedback):
        delimiter = '\n===\n'
        prompt = self.fixer_prompt + '\nTask statement:\n' + task
        prompt = prompt + delimiter + 'Solution:\n' + solution
        prompt = prompt + delimiter + 'Fixer feedback:\n' + feedback
        return prompt
    
    def fix(self, task, solution, feedback):
        prompt = self._make_fixer_prompt(task, solution, feedback)
        self._log(f'Sending response to llm with prompt: {prompt}')
        response = self._send_request(prompt)
        if response['content']:
            self._log(f'Recived fixes from llm:\n{response}')
            solution = self._parse_response(response['content'])
            self._log(f'Recived feedback summary from llm:\n{solution['feedback_summary']}')
            self._log(f'Recived corrected solution from llm:\n{solution['corrected_solution']}')
            self._log(f'Recived corrected answer from llm:\n{solution['corrected_answer']}')
            return solution
        else:
            raise RuntimeError(f'error during solving task {response['error']}')
    
    
    
