from agent import Agent
from logTools import LogLevel


class Checker(Agent):
    def __init__(self, log_level):
        super().__init__(log_level)

        self.sys_prompt = self._read_sys_prompt('prompts/checker.txt')
        self.agent_name = 'Checker'
        self.color = 'magenta'

    def _parse_response(self, llm_response):
        return self.response_parser.parse_checker_response(llm_response)

    def check(self, solution, answer):
        prompt = self.sys_prompt + solution + '\nAnswer is:\n' + answer
        self._log(LogLevel.RELEASE, f'Sending request to llm...')
        self._log(LogLevel.DEBUG, f'Checker prompt: {prompt}')
        response = self._send_request(prompt)
        if response['content']:
            self._log(LogLevel.DEBUG, f'Recived review from llm:\n{response}')
            self._log(LogLevel.RELEASE, f'Parsing response...')
            solution = self._parse_response(response['content'])
            self._log(LogLevel.DEBUG, f'Recived analysis from llm:\n{solution['analysis']}')
            self._log(LogLevel.DEBUG, f'Recived issues from llm:\n{solution['issues']}')
            self._log(LogLevel.RELEASE, f'Recived verdict from llm: {solution['verdict']}')
            return solution
        else:
            raise RuntimeError(f'error during solving task {response['error']}')
