import os

API_KEY_ENV = "API_KEY"
API_KEY_FILE = "../api-key"

def get_llm_api_key() -> str:
    all_env_vars = os.environ
    if API_KEY_ENV in all_env_vars:
        return all_env_vars[API_KEY_ENV]

    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE) as file:
            return file.read()

    raise RuntimeError("No LLM API key is found")
