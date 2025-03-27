from .base_agent import BaseAgent
import re
import json
import logging
from omegaconf import DictConfig
from pydantic import BaseModel 

class CleaningOutput(BaseModel):
    cleaned_text: str

class CleaningAgent(BaseAgent):
    def __init__(self, cfg: DictConfig):
        super().__init__(cfg)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Cleaning agent initialized")
    
    def analyze(self, text):
        self.logger.info("Cleaning text using regex and Llama")
        
        cleaned_text = re.sub(r'\s+', ' ', text)  
        cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text)  # Remove punctuations
        
        system_prompt = self.prompts.CLEANING_SYSTEM
        user_prompt = self.prompts.CLEANING_USER.format(text=cleaned_text)
        
        try:
            result = self.query_llm(system_prompt, user_prompt, schema=CleaningOutput)
            final_cleaned_text = result.cleaned_text  
            return final_cleaned_text
        except (json.JSONDecodeError, AttributeError) as e:
            self.logger.error(f"Failed to parse LLM response: {e}")
            return text  