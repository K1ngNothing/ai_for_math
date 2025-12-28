from agent import Agent


class Checker(Agent):
    def __init__(self):
        super().__init__()
        
        self.sys_prompt = self._read_sys_prompt('prompts/checker.txt')
        self.agent_name = 'Checker'
        self.color = 'magenta'
        
    def _parse_response(self, llm_response):
        return self.response_parser.parse_checker_response(llm_response)
    
    def check(self, solution, answer):
        prompt = self.sys_prompt + solution + '\nAnswer is:\n' + answer
        self._log(f'Sending response to llm with prompt: {prompt}')
        response = self._send_request(prompt)
        if response['content']:
            self._log(f'Recived review from llm:\n{response}')
            solution = self._parse_response(response['content'])
            self._log(f'Recived analysis from llm:\n{solution['analysis']}')
            self._log(f'Recived issues from llm:\n{solution['issues']}')
            self._log(f'Recived verdict from llm:\n{solution['verdict']}')
            return solution
        else:
            raise RuntimeError(f'error during solving task {response['error']}')
    
