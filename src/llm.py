import requests
from enum import Enum
from utils import get_llm_api_key


class ResponseStatus(str, Enum):
    OK = 'OK'
    ERROR = 'ERROR'

class LLM:
    def __init__(
        self,
        api_key,
        model,
        temperature=None,
        host='https://openai.api.proxyapi.ru/v1',
        timeout=360,
        reasoning_effort=None,
    ):
        self.host = host.rstrip('/')
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.temperature = temperature
        self.reasoning_effort = reasoning_effort
        self.headers = {
            'Content-Type': 'application/json'
        }

        if self.api_key:
            self.headers['Authorization'] = f'Bearer {self.api_key}'

    @staticmethod
    def _extract_responses_text(result):
        """Extracts text from /responses API"""
        if result.get('output_text'):
            return result['output_text'].strip()

        output_items = result.get('output', [])
        text_parts = []

        for item in output_items:
            for content_item in item.get('content', []):
                if content_item.get('type') == 'output_text':
                    text_parts.append(content_item.get('text', ''))

        return ''.join(text_parts).strip()

    def send_request(self, prompt, max_tokens = 8192):
        try:
            chain_of_thoughts_enabled = self.reasoning_effort is not None
            if not chain_of_thoughts_enabled:
                # Old API
                messages = []
                messages.append({'role': 'user', 'content': prompt})

                payload = {
                    'model': self.model,
                    'messages': messages,
                    'max_tokens': max_tokens
                }
                if self.temperature is not None:
                    payload['temperature'] = self.temperature

                response = requests.post(
                    f'{self.host}/chat/completions',
                    headers=self.headers,
                    json=payload,
                    timeout=self.timeout
                )
            else:
                # New /responses API
                payload = {
                    'model': self.model,
                    'input': [
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    'max_output_tokens': max_tokens,
                    'reasoning': {'effort': self.reasoning_effort}
                }

                response = requests.post(
                    f'{self.host}/responses',
                    headers=self.headers,
                    json=payload,
                    timeout=self.timeout
                )

            response.raise_for_status()

            result = response.json()
            if chain_of_thoughts_enabled:
                content = self._extract_responses_text(result)
            else:
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
