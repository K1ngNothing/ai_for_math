from agent import Agent
from logTools import LogLevel


class Verificator(Agent):
    def __init__(self, log_level):
        super().__init__(log_level)

        self.verificator_prompt = self._read_sys_prompt('prompts/verificator.txt')
        self.agent_name = 'Verificator'
        self.color = 'yellow'

    def _parse_response(self, llm_response):
        return self.response_parser.parse_verificator_response(llm_response)

    def verify(self, expected_answer, actual_answer):
        prompt = self.verificator_prompt
        prompt += '\nExpected answer:\n' + str(expected_answer)
        prompt += '\n===\nActual answer:\n' + str(actual_answer)
        self._log(LogLevel.RELEASE, 'Sending request to llm...')
        self._log(LogLevel.DEBUG, f'Verificator prompt: {prompt}')
        response = self._send_request(prompt)
        if response['content']:
            self._log(LogLevel.DEBUG, f'Received verification from llm:\n{response}')
            self._log(LogLevel.RELEASE, 'Parsing response...')
            verdict = self._parse_response(response['content'])
            self._log(LogLevel.RELEASE, f'Received verdict from llm: {verdict["verdict"]}')
            return verdict
        else:
            raise RuntimeError(f'error during verification {response["error"]}')
