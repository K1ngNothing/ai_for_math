from llm import LLM
from parser import ResponseParser
from logTools import COLOR_CODES


class Agent:
    def __init__(self, log_level):
        self.agent_name = ''
        self.color = ''
        self.log_level = log_level

        self.response_parser = ResponseParser()
        api_key = ''
        with open('../api-key') as file:
            api_key = file.read()
        # self.llm =  LLM(api_key=api_key, model='gemini/gemini-3-flash-preview', temperature=1.0)
        self.llm =  LLM(api_key=api_key, model='openai/gpt-4.1', temperature=0.7)
        # self.llm =  LLM(api_key=api_key, model='openai/gpt-4.1-mini', temperature=0.7)

    def _read_sys_prompt(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")

    def _send_request(self, prompt):
        return self.llm.send_request(prompt)

    def _log(self, level, info):
        if level > self.log_level:
            return

        import time
        current_time = time.strftime('%H:%M:%S')
        print(f"[{current_time}]{COLOR_CODES.get(self.color, '')}[{self.agent_name}]: {info}\033[0m")
