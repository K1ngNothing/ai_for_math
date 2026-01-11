import requests
from enum import Enum
from utils import get_llm_api_key


class ResponseStatus(str, Enum):
    OK = 'OK'
    ERROR = 'ERROR'

class LLM:
    def __init__(self, api_key, model, temperature,  host = 'https://openai.api.proxyapi.ru/v1', timeout = 360):
        self.host = host.rstrip('/')
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.temperature = temperature
        self.headers = {
            'Content-Type': 'application/json'
        }

        if self.api_key:
            self.headers['Authorization'] = f'Bearer {self.api_key}'

    def send_request(self, prompt, max_tokens = 8192):
        try:
            messages = []
            messages.append({'role': 'user', 'content': prompt})

            payload = {
                'model': self.model,
                'messages': messages,
                'max_tokens': max_tokens
            }
            if self.temperature:
                payload['temperature'] = self.temperature

            response = requests.post(
                f'{self.host}/chat/completions',
                headers=self.headers,
                json=payload,
                timeout=self.timeout
            )

            response.raise_for_status()

            result = response.json()
            content = result['choices'][0]['message']['content'].strip()

            return {
                'status': ResponseStatus.OK,
                'content': content
            }

        except requests.exceptions.Timeout:
            raise RuntimeError('timeout expired')


if __name__ == '__main__':
    api_key = get_llm_api_key()
    llm = LLM(api_key=api_key, model='gemini/gemini-3-flash-preview', temperature=1.0)
    prompt = "HI! please, write Hello world program on c++"
    response = llm.send_request(prompt)
    print(response)
