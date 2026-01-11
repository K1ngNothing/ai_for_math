from agent import Agent
from logTools import LogLevel


class Fixer(Agent):
    def __init__(self, log_level):
        super().__init__(log_level)

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
        self._log(LogLevel.RELEASE, f'Sending request to llm...')
        self._log(LogLevel.DEBUG, f'Fixer prompt: {prompt}')
        response = self._send_request(prompt)
        if response['content']:
            self._log(LogLevel.DEBUG, f'Recived fixes from llm:\n{response}')
            self._log(LogLevel.RELEASE, f'Parsing response...')
            solution = self._parse_response(response['content'])
            self._log(LogLevel.DEBUG, f'Recived feedback summary from llm:\n{solution['feedback']}')
            self._log(LogLevel.DEBUG, f'Recived corrected solution from llm:\n{solution['solution']}')
            self._log(LogLevel.RELEASE, f'Recived corrected answer from llm: {solution['answer']}')
            return solution
        else:
            raise RuntimeError(f'error during solving task {response['error']}')
