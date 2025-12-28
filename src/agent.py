from llm import LLM
from parser import ResponseParser

class Agent:
    def __init__(self):
        self.agent_name = ''
        self.color = ''
        
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

    def _log(self, info):
        import time
        color_codes = {
            'red': '\033[91m', 
            'green': '\033[92m', 
            'yellow': '\033[93m', 
            'blue': '\033[94m', 
            'magenta': '\033[95m', 
            'cyan': '\033[96m'
        }
        current_time = time.strftime('%H:%M:%S')
        print(f"{color_codes.get(self.color, '')}[{current_time}][{self.agent_name}]: {info}\033[0m")
