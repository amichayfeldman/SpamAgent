import requests
import json
from ollama import chat
import logging
from omegaconf import DictConfig
from prompts import Prompts
import re

class BaseAgent:
    def __init__(self, cfg: DictConfig):
        self.cfg = cfg
        self.model_name = cfg.model.name
        self.prompts = Prompts()
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def query_llm(self,
                  system_prompt, 
                  user_prompt, 
                  schema=None):
        try:
            response = chat(model=self.model_name,
                            messages=[{"role": "system",
                                        "content": system_prompt},
                                    {"role": "user",
                                        "content": user_prompt}])#,
                #    format=TaskAnalyzerResponse.model_json_schema())
            match = re.search(r'```(.*?)```', response.message.content, re.DOTALL)
            parsed_ans = json.loads(match.group(1).strip())
            return parsed_ans
        except requests.Timeout:
            self.logger.error(f"Request timed out after {self.timeout} seconds")
            raise Exception(f"Request timed out after {self.timeout} seconds")
        except Exception as e:
            self.logger.error(f"Error during LLM query: {str(e)}")
            raise
    
    def analyze(self, text):
        raise NotImplementedError("Subclasses must implement analyze method") 