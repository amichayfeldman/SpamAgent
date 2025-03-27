import pyrootutils
root  = pyrootutils.setup_root(__file__, 
                               pythonpath=True,
                               cwd=True)
import requests
import json
from ollama import chat
import logging
from omegaconf import DictConfig
from src.prompts import Prompts
import re
import os
from pydantic import BaseModel, ValidationError  # Import Pydantic

def validate_parentheses(text):
    if not text:
        return text
    
    stack = []
    for char in text:
        if char == '{':
            stack.append(char)
        elif char == '}':
            if stack and stack[-1] == '{':
                stack.pop()
            else:
                pass
    
    # Add missing closing parentheses
    result = text
    for _ in range(len(stack)):
        result += '}'
    
    return result

class BaseAgent:
    def __init__(self, cfg: DictConfig):
        self.cfg = cfg
        self.model_name = cfg["model"]["name"]
        self.prompts = Prompts()
        self.logger = logging.getLogger(self.__class__.__name__)
        
        self.ollama_host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        os.environ["OLLAMA_HOST"] = self.ollama_host
    
    def query_llm(self,
                  system_prompt, 
                  user_prompt, 
                  schema=None):
        try:
            payload = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            }
            if schema:
                payload.update({"format": schema.model_json_schema()})
            # response = requests.post(f"{self.ollama_host}/api/chat", json=payload)
            response_data = chat(**payload)
            # response.raise_for_status()
            # response_data = response.json()
            ans = response_data["message"]["content"].replace("\n", "")
            self.logger.info(ans)
            ans = validate_parentheses(ans)

            if schema:
                parsed_ans = schema.model_validate_json(ans)
            else:
                parsed_ans = eval(ans) 
        except ValidationError as e:
            self.logger.error(f"Validation error: {e}")
            raise
        except SyntaxError as e:
            match = re.search(r'```(.*?)```', ans, re.DOTALL)
            parsed_ans = json.loads(match.group(1).strip())
        except Exception as e:
            self.logger.error(f"Error during LLM query: {str(e)}")
            raise
        return parsed_ans
    
    def analyze(self, text):
        raise NotImplementedError("Subclasses must implement analyze method") 